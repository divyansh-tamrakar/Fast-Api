"""adding columns to post table

Revision ID: ea8c02959b2d
Revises: c109d24f88e2
Create Date: 2022-10-03 18:43:22.026928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea8c02959b2d'
down_revision = 'c109d24f88e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
