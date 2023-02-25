"""add last few columns to post table

Revision ID: 41042e903d76
Revises: de6068042242
Create Date: 2023-02-23 22:43:56.463106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41042e903d76'
down_revision = 'de6068042242'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default='True', nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
