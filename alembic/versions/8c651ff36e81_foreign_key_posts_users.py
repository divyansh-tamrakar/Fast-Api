"""foreign key posts->users

Revision ID: 8c651ff36e81
Revises: e000c24dbced
Create Date: 2022-10-04 16:06:31.236611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c651ff36e81'
down_revision = 'e000c24dbced'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
