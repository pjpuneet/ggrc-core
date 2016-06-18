# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Initial ggrc_workflows migration

Revision ID: 1d33919af441
Revises: None
Create Date: 2014-05-29 01:00:47.198955

"""

# revision identifiers, used by Alembic.
revision = '1d33919af441'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('end_date', sa.Date(), nullable=True),
      sa.Column('start_date', sa.Date(), nullable=True),
      sa.Column('description', sa.Text(), nullable=True),
      sa.Column('title', sa.String(length=250), nullable=False),
      sa.Column('slug', sa.String(length=250), nullable=False),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_tasks_context_id'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('slug', name='uq_tasks'),
      sa.UniqueConstraint('title', name='uq_t_tasks')
      )
    op.create_index('fk_tasks_contexts', 'tasks', ['context_id'], unique=False)

    op.create_table('task_entries',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('description', sa.Text(), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_task_entries_context_id'),
      sa.PrimaryKeyConstraint('id')
      )
    op.create_index('fk_task_entries_contexts', 'task_entries', ['context_id'], unique=False)

    op.create_table('workflows',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('end_date', sa.Date(), nullable=True),
      sa.Column('start_date', sa.Date(), nullable=True),
      sa.Column('description', sa.Text(), nullable=True),
      sa.Column('title', sa.String(length=250), nullable=False),
      sa.Column('slug', sa.String(length=250), nullable=False),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_workflows_context_id'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('slug', name='uq_workflows'),
      sa.UniqueConstraint('title', name='uq_t_workflows')
      )
    op.create_index('fk_workflows_contexts', 'workflows', ['context_id'], unique=False)

    op.create_table('workflow_people',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('workflow_id', sa.Integer(), nullable=False),
      sa.Column('person_id', sa.Integer(), nullable=False),
      sa.Column('status', sa.String(length=250), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_workflow_people_context_id'),
      sa.ForeignKeyConstraint(['person_id'], ['people.id'], name='fk_workflow_people_person_id'),
      sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], name='fk_workflow_people_workflow_id'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('workflow_id', 'person_id')
      )
    op.create_index('fk_workflow_people_contexts', 'workflow_people', ['context_id'], unique=False)
    op.create_index('ix_person_id', 'workflow_people', ['person_id'], unique=False)
    op.create_index('ix_workflow_id', 'workflow_people', ['workflow_id'], unique=False)

    op.create_table('workflow_tasks',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('workflow_id', sa.Integer(), nullable=False),
      sa.Column('task_id', sa.Integer(), nullable=False),
      sa.Column('end_date', sa.Date(), nullable=True),
      sa.Column('start_date', sa.Date(), nullable=True),
      sa.Column('status', sa.String(length=250), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_workflow_tasks_context_id'),
      sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_workflow_tasks_task_id'),
      sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], name='fk_workflow_tasks_workflow_id'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('workflow_id', 'task_id')
      )
    op.create_index('fk_workflow_tasks_contexts', 'workflow_tasks', ['context_id'], unique=False)

    op.create_table('task_groups',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('workflow_id', sa.Integer(), nullable=False),
      sa.Column('contact_id', sa.Integer(), nullable=True),
      sa.Column('end_date', sa.Date(), nullable=True),
      sa.Column('start_date', sa.Date(), nullable=True),
      sa.Column('description', sa.Text(), nullable=True),
      sa.Column('title', sa.String(length=250), nullable=False),
      sa.Column('slug', sa.String(length=250), nullable=False),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['contact_id'], ['people.id'], name='fk_task_groups_contact_id'),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_task_groups_context_id'),
      sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], name='fk_task_groups_workflow_id'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('slug', name='uq_task_groups'),
      sa.UniqueConstraint('title', name='uq_t_task_groups')
      )
    op.create_index('fk_task_groups_contact', 'task_groups', ['contact_id'], unique=False)
    op.create_index('fk_task_groups_contexts', 'task_groups', ['context_id'], unique=False)

    op.create_table('workflow_objects',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('workflow_id', sa.Integer(), nullable=False),
      sa.Column('object_id', sa.Integer(), nullable=False),
      sa.Column('object_type', sa.String(length=250), nullable=False),
      sa.Column('end_date', sa.Date(), nullable=True),
      sa.Column('start_date', sa.Date(), nullable=True),
      sa.Column('status', sa.String(length=250), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_workflow_objects_context_id'),
      sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], name='fk_workflow_objects_workflow_id'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('workflow_id', 'object_id', 'object_type')
      )
    op.create_index('fk_workflow_objects_contexts', 'workflow_objects', ['context_id'], unique=False)
    op.create_index('ix_workflow_id', 'workflow_objects', ['workflow_id'], unique=False)

    op.create_table('task_group_objects',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('task_group_id', sa.Integer(), nullable=False),
      sa.Column('object_id', sa.Integer(), nullable=False),
      sa.Column('object_type', sa.String(length=250), nullable=False),
      sa.Column('end_date', sa.Date(), nullable=True),
      sa.Column('start_date', sa.Date(), nullable=True),
      sa.Column('status', sa.String(length=250), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_task_group_objects_context_id'),
      sa.ForeignKeyConstraint(['task_group_id'], ['task_groups.id'], name='fk_task_group_objects_task_group_id'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('task_group_id', 'object_id', 'object_type')
      )
    op.create_index('fk_task_group_objects_contexts', 'task_group_objects', ['context_id'], unique=False)
    op.create_index('ix_task_group_id', 'task_group_objects', ['task_group_id'], unique=False)

    op.create_table('task_group_tasks',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('task_group_id', sa.Integer(), nullable=False),
      sa.Column('task_id', sa.Integer(), nullable=False),
      sa.Column('end_date', sa.Date(), nullable=True),
      sa.Column('start_date', sa.Date(), nullable=True),
      sa.Column('status', sa.String(length=250), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], name='fk_task_group_tasks_context_id'),
      sa.ForeignKeyConstraint(['task_group_id'], ['task_groups.id'], name='fk_task_group_tasks_task_group_id'),
      sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_task_group_tasks_task_id'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('task_group_id', 'task_id')
      )
    op.create_index('fk_task_group_tasks_contexts', 'task_group_tasks', ['context_id'], unique=False)


def downgrade():
    op.drop_constraint('fk_task_group_tasks_context_id', 'task_group_tasks', type_='foreignkey')
    op.drop_index('fk_task_group_tasks_contexts', table_name='task_group_tasks')
    op.drop_table('task_group_tasks')

    op.drop_index('ix_task_group_id', table_name='task_group_objects')
    op.drop_constraint('fk_task_group_objects_context_id', 'task_group_objects', type_='foreignkey')
    op.drop_index('fk_task_group_objects_contexts', table_name='task_group_objects')
    op.drop_table('task_group_objects')

    op.drop_index('ix_workflow_id', table_name='workflow_objects')
    op.drop_constraint('fk_workflow_objects_context_id', 'workflow_objects', type_='foreignkey')
    op.drop_index('fk_workflow_objects_contexts', table_name='workflow_objects')
    op.drop_table('workflow_objects')

    op.drop_constraint('fk_task_groups_context_id', 'task_groups', type_='foreignkey')
    op.drop_index('fk_task_groups_contexts', table_name='task_groups')
    op.drop_constraint('fk_task_groups_contact_id', 'task_groups', type_='foreignkey')
    op.drop_index('fk_task_groups_contact', table_name='task_groups')
    op.drop_table('task_groups')

    op.drop_constraint('fk_workflow_tasks_context_id', 'workflow_tasks', type_='foreignkey')
    op.drop_index('fk_workflow_tasks_contexts', table_name='workflow_tasks')
    op.drop_table('workflow_tasks')

    op.drop_index('ix_workflow_id', table_name='workflow_people')
    op.drop_constraint('fk_workflow_people_person_id', 'workflow_people', type_='foreignkey')
    op.drop_index('ix_person_id', table_name='workflow_people')
    op.drop_constraint('fk_workflow_people_context_id', 'workflow_people', type_='foreignkey')
    op.drop_index('fk_workflow_people_contexts', table_name='workflow_people')
    op.drop_table('workflow_people')

    op.drop_constraint('fk_workflows_context_id', 'workflows', type_='foreignkey')
    op.drop_index('fk_workflows_contexts', table_name='workflows')
    op.drop_table('workflows')

    op.drop_constraint('fk_task_entries_context_id', 'task_entries', type_='foreignkey')
    op.drop_index('fk_task_entries_contexts', table_name='task_entries')
    op.drop_table('task_entries')

    op.drop_constraint('fk_tasks_context_id', 'tasks', type_='foreignkey')
    op.drop_index('fk_tasks_contexts', table_name='tasks')
    op.drop_table('tasks')
