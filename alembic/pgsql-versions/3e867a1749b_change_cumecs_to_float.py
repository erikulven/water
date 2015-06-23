"""change cumecs to float

Revision ID: 3e867a1749b
Revises: 132e1596946
Create Date: 2015-06-21 10:25:50.752381

"""

# revision identifiers, used by Alembic.
revision = '3e867a1749b'
down_revision = '132e1596946'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('measures', 'cumecs',
                    existing_type=sa.INTEGER(),
                    type_=sa.Float(),
                    existing_nullable=False)

    op.create_index(op.f('ix_measure_measured_at'), 'measures',
                    ['river_id', 'measured_at'],
                    unique=False)


def downgrade():
    op.alter_column('measures', 'cumecs',
                    existing_type=sa.Float(),
                    type_=sa.INTEGER(),
                    existing_nullable=False)
    op.drop_index(op.f('ix_measure_measured_at'), table_name='measures')
