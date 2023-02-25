"""add foregin key to post table

Revision ID: de6068042242
Revises: e28aa4b41190
Create Date: 2023-02-23 22:25:21.011685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de6068042242'
down_revision = 'e28aa4b41190'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key('post_user_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint("post_user_fkey", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
