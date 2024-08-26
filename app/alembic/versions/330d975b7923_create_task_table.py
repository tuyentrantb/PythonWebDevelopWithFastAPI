"""create task table

Revision ID: 330d975b7923
Revises: e20751e7718a
Create Date: 2024-08-26 18:24:24.017729

"""
from alembic import op
import sqlalchemy as sa
from schemas.task import TaskStatus


# revision identifiers, used by Alembic.
revision = '330d975b7923'
down_revision = 'e20751e7718a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('summary', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('status', sa.Enum(TaskStatus), nullable=False, default=TaskStatus.NEW),
        sa.Column('priority', sa.SmallInteger, default=0),
        sa.Column('user_id', sa.UUID, nullable=False)
    )
    op.create_foreign_key('fk_task_user', 'tasks', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    op.drop_table('tasks')

