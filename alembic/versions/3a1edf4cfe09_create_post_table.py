"""create post table

Revision ID: 3a1edf4cfe09
Revises: 
Create Date: 2023-02-23 18:30:18.989305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a1edf4cfe09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer, nullable=False, primary_key=True)
                    , sa.Column('title', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
