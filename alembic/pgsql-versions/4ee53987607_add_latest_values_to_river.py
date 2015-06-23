"""add latest values to river

Revision ID: 4ee53987607
Revises: 1ac68e11655
Create Date: 2015-06-21 21:06:03.278745

"""

# revision identifiers, used by Alembic.
revision = '4ee53987607'
down_revision = '1ac68e11655'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('rivers', sa.Column('latest_cumecs', sa.Float(), nullable=True))
    op.add_column('rivers', sa.Column('latest_level', sa.String(length=20), nullable=True))


def downgrade():
    op.drop_column('rivers', 'latest_level')
    op.drop_column('rivers', 'latest_cumecs')
