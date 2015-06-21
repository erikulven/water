"""fix typo latest measure in river

Revision ID: 1ac68e11655
Revises: 553e3a9bb6
Create Date: 2015-06-21 11:12:47.157724

"""

# revision identifiers, used by Alembic.
revision = '1ac68e11655'
down_revision = '553e3a9bb6'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('rivers', sa.Column('latest_measure_at', sa.DateTime(), nullable=True))
    op.drop_column('rivers', 'latest_mesasure_at')


def downgrade():
    op.add_column('rivers', sa.Column('latest_mesasure_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('rivers', 'latest_measure_at')
