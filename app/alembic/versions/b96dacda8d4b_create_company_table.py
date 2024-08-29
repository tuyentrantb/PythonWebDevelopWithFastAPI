"""create company table

Revision ID: b96dacda8d4b
Revises: 
Create Date: 2024-08-26 14:50:21.718220

"""
from alembic import op
import sqlalchemy as sa
from schemas.company import CompanyMode


# revision identifiers, used by Alembic.
revision = 'b96dacda8d4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.Enum(CompanyMode), nullable=False, default=CompanyMode.DRAFT),
        sa.Column('rating', sa.SmallInteger, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('companies')
    op.execute("DROP TYPE companymode;")
