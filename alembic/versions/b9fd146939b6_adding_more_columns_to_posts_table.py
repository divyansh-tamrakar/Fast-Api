"""adding more columns to posts table

Revision ID: b9fd146939b6
Revises: 8c651ff36e81
Create Date: 2022-10-04 16:13:44.807474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9fd146939b6'
down_revision = '8c651ff36e81'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
