# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Methods to create expected workflow cycle entities from workflow entities.
"""
from lib.constants import object_states
from lib.entities import app_entity_factory


def create_workflow_cycle(workflow):
  """Creates expected WorkflowCycle entity from Workflow entity."""
  cycle_task_groups = [_create_from_task_group(task_group)
                       for task_group in workflow.task_groups]
  cycle_tasks = [cycle_task for cycle_task_group in cycle_task_groups
                 for cycle_task in cycle_task_group.cycle_tasks]
  return app_entity_factory.WorkflowCycleFactory().create_empty(
      title=workflow.title,
      admins=workflow.admins,
      wf_members=workflow.wf_members,
      state=object_states.ASSIGNED,
      due_date=max(cycle_task.due_date for cycle_task in cycle_tasks),
      cycle_task_groups=cycle_task_groups,
      workflow=workflow
  )


def _create_from_task_group(task_group):
  """Creates expected CycleTaskGroup entity from TaskGroup entity."""
  cycle_tasks = [_create_from_task(task)
                 for task in task_group.task_group_tasks]
  return app_entity_factory.CycleTaskGroupFactory().create_empty(
      title=task_group.title,
      state=object_states.ASSIGNED,
      cycle_tasks=cycle_tasks,
      task_group=task_group
  )


def _create_from_task(task_group_task):
  """Creates expected CycleTask entity from TaskGroupTask entity."""
  return app_entity_factory.CycleTaskFactory().create_empty(
      title=task_group_task.title,
      state=object_states.ASSIGNED,
      due_date=task_group_task.due_date,
      task_group_task=task_group_task
  )
