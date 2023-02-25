"""add content column in post table

Revision ID: 8a037ba9a616
Revises: 3a1edf4cfe09
Create Date: 2023-02-23 19:20:22.910096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a037ba9a616'
down_revision = '3a1edf4cfe09'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
