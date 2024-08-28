"""create user table

Revision ID: e20751e7718a
Revises: b96dacda8d4b
Create Date: 2024-08-26 17:53:29.093633

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from schemas.user import get_password_hash
from settings import DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision = 'e20751e7718a'
down_revision = 'b96dacda8d4b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column('company_id', sa.UUID, nullable=True)
    )
    op.create_index("idx_usr_fst_lst_name", "users", ["first_name", "last_name"])
    op.create_foreign_key('fk_user_company', 'users', 'companies', ['company_id'], ['id'])
    
    # Data seed for first user
    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "email": "fastapi_tour@sample.com", 
            "username": "fa_admin",
            "hashed_password": get_password_hash(DEFAULT_PASSWORD),
            "first_name": "FastApi",
            "last_name": "Admin",
            "is_active": True,
            "is_admin": True
        }
    ])

def downgrade() -> None:
    op.drop_table("users")
