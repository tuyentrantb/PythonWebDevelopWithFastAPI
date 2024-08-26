"""create user table

Revision ID: e20751e7718a
Revises: b96dacda8d4b
Create Date: 2024-08-26 17:53:29.093633

"""
from uuid import uuid4
from datetime import datetime, timezone
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e20751e7718a'
down_revision = 'b96dacda8d4b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column('company_id', sa.UUID, nullable=False)
    )
    op.create_index("idx_usr_fst_lst_name", "users", ["first_name", "last_name"])
    op.create_foreign_key('fk_user_company', 'users', 'companies', ['company_id'], ['id'])

def downgrade() -> None:
    op.drop_table("users")
