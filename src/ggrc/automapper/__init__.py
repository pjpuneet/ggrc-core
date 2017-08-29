# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Automapper generator."""

from datetime import datetime
from logging import getLogger
import collections

from sqlalchemy.sql.expression import tuple_

from ggrc import db
from ggrc.automapper import rules
from ggrc.login import get_current_user
from ggrc.models.automapping import Automapping
from ggrc.models.relationship import Relationship
from ggrc.rbac.permissions import is_allowed_update
from ggrc.services.common import get_cache
from ggrc.services import signals
from ggrc.utils import benchmark, with_nop


# pylint: disable=invalid-name
logger = getLogger(__name__)


class Stub(collections.namedtuple("Stub", ["type", "id"])):
  """Minimal object representation."""

  @classmethod
  def from_source(cls, relationship):
    return Stub(relationship.source_type, relationship.source_id)

  @classmethod
  def from_destination(cls, relationship):
    return Stub(relationship.destination_type, relationship.destination_id)


class AutomapperGenerator(object):
  """Generator for automappings.

  Consumes automapping rules and newly created Relationships, creates
  autogenerated Relationships registering them in Automappings table.
  """

  COUNT_LIMIT = 10000

  def __init__(self, use_benchmark=True):
    self.processed = set()
    self.queue = set()
    self.cache = collections.defaultdict(set)
    self.auto_mappings = set()
    if use_benchmark:
      self.benchmark = benchmark
    else:
      self.benchmark = with_nop

  def related(self, obj):
    if obj in self.cache:
      return self.cache[obj]
    # Pre-fetch neighborhood for enqueued object since we're gonna need that
    # results in a few steps. This drastically reduces number of queries.
    stubs = {s for rel in self.queue for s in rel}
    stubs.add(obj)
    # Union is here to convince mysql to use two separate indices and
    # merge te results. Just using `or` results in a full-table scan
    # Manual column list avoids loading the full object which would also try to
    # load related objects
    cols = db.session.query(
        Relationship.source_type, Relationship.source_id,
        Relationship.destination_type, Relationship.destination_id)
    relationships = cols.filter(
        tuple_(Relationship.source_type, Relationship.source_id).in_(
            [(s.type, s.id) for s in stubs]
        )
    ).union_all(
        cols.filter(
            tuple_(Relationship.destination_type,
                   Relationship.destination_id).in_(
                       [(s.type, s.id) for s in stubs]))
    ).all()
    for (src_type, src_id, dst_type, dst_id) in relationships:
      src = Stub(src_type, src_id)
      dst = Stub(dst_type, dst_id)
      # only store a neighbor if we queried for it since this way we know
      # we'll be storing complete neighborhood by the end of the loop
      if src in stubs:
        self.cache[src].add(dst)
      if dst in stubs:
        self.cache[dst].add(src)

    return self.cache[obj]

  @staticmethod
  def order(src, dst):
    return (src, dst) if src < dst else (dst, src)

  def generate_automappings(self, relationship):
    self.auto_mappings = set()
    with self.benchmark("Automapping generate_automappings"):
      # initial relationship is special since it is already created and
      # processing it would abort the loop so we manually enqueue the
      # neighborhood
      src = Stub.from_source(relationship)
      dst = Stub.from_destination(relationship)
      self._step(src, dst)
      self._step(dst, src)
      while self.queue:
        if len(self.auto_mappings) > self.COUNT_LIMIT:
          break
        src, dst = entry = self.queue.pop()

        if not (self._can_map_to(src, relationship) and
                self._can_map_to(dst, relationship)):
          continue

        created = self._ensure_relationship(src, dst)
        self.processed.add(entry)
        if not created:
          # If the edge already exists it means that auto mappings for it have
          # already been processed and it is safe to cut here.
          continue
        self._step(src, dst)
        self._step(dst, src)

      if len(self.auto_mappings) <= self.COUNT_LIMIT:
        self._flush(relationship)
      else:
        relationship._json_extras = {
            'automapping_limit_exceeded': True
        }

  @staticmethod
  def _can_map_to(obj, parent_relationship):
    return is_allowed_update(obj.type, obj.id, parent_relationship.context)

  def _flush(self, parent_relationship):
    """Manually INSERT generated automappings."""
    if not self.auto_mappings:
      return
    with self.benchmark("Automapping flush"):
      current_user = get_current_user()
      automapping = Automapping(parent_relationship)
      db.session.add(automapping)
      db.session.flush()
      now = datetime.now()
      # We are doing an INSERT IGNORE INTO here to mitigate a race condition
      # that happens when multiple simultaneous requests create the same
      # automapping. If a relationship object fails our unique constraint
      # it means that the mapping was already created by another request
      # and we can safely ignore it.
      inserter = Relationship.__table__.insert().prefix_with("IGNORE")
      original = self.order(Stub.from_source(parent_relationship),
                            Stub.from_destination(parent_relationship))
      db.session.execute(inserter.values([{
          "id": None,
          "modified_by_id": current_user.id,
          "created_at": now,
          "updated_at": now,
          "source_id": src.id,
          "source_type": src.type,
          "destination_id": dst.id,
          "destination_type": dst.type,
          "context_id": None,
          "status": None,
          "parent_id": parent_relationship.id,
          "automapping_id": automapping.id}
          for src, dst in self.auto_mappings
          if (src, dst) != original]))  # (src, dst) is sorted
      cache = get_cache(create=True)
      if cache:
        # Add inserted relationships into new objects collection of the cache,
        # so that they will be logged within event and appropriate revisions
        # will be created.
        cache.new.update(
            (relationship, relationship.log_json())
            for relationship in Relationship.query.filter_by(
                parent_id=parent_relationship.id,
                modified_by_id=current_user.id,
                created_at=now,
                updated_at=now,
            )
        )

  def _step(self, src, dst):
    mappings = rules.rules[src.type, dst.type]
    if mappings:
      src_related = (o for o in self.related(src)
                     if o.type in mappings and o != dst)
      for r in src_related:
        entry = self.order(r, dst)
        if entry not in self.processed:
          self.queue.add(entry)

  def _ensure_relationship(self, src, dst):
    """Create the relationship if not exists already.

    Returns:
      True if a relationship was created;
      False otherwise.
    """
    # even though self.cache is defaultdict, self.cache[key] adds key
    # to self.cache if it is not present, and we should avoid it
    if dst in self.cache.get(src, set()):
      return False
    if src in self.cache.get(dst, set()):
      return False

    self.auto_mappings.add((src, dst))

    if src in self.cache:
      self.cache[src].add(dst)
    if dst in self.cache:
      self.cache[dst].add(src)

    return True


def register_automapping_listeners():
  """Register event listeners for auto mapper."""
  # pylint: disable=unused-variable,unused-argument

  @signals.Restful.collection_posted.connect_via(Relationship)
  def handle_relationship_collection_post(sender, objects=None, **kwargs):
    """Handle bulk creation of relationships.

    This handler reuses auto mapper cache and is more efficient than handling
    one object at a time.

    Args:
      objects: list of relationship Models.
    """
    automapper = AutomapperGenerator()
    for obj in objects:
      if obj is None:
        logger.warning("Automapping listener: no obj, no mappings created")
        return
      automapper.generate_automappings(obj)
