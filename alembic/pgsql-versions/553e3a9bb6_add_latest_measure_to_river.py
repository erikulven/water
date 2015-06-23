"""add latest measure to river

Revision ID: 553e3a9bb6
Revises: 3e867a1749b
Create Date: 2015-06-21 10:37:46.920118

"""

# revision identifiers, used by Alembic.
revision = '553e3a9bb6'
down_revision = '3e867a1749b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('rivers',
                  sa.Column('latest_mesasure_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('rivers', 'latest_mesasure_at')
