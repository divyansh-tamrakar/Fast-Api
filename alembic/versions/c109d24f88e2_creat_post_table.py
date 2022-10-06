"""creat post table

Revision ID: c109d24f88e2
Revises: 
Create Date: 2022-10-03 18:13:07.468452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c109d24f88e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts", "app.schemas.PostBase")
    pass
