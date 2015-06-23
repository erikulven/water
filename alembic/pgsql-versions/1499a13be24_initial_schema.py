"""initial schema

Revision ID: 1499a13be24
Revises: None
Create Date: 2015-06-20 09:25:20.681949

"""

# revision identifiers, used by Alembic.
revision = '1499a13be24'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('rivers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('identifier', sa.String(length=255),
                              nullable=False),
                    sa.Column('source', sa.String(length=255), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('identifier'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('measures',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('measured_at', sa.DateTime(), nullable=False),
                    sa.Column('level', sa.String(length=20), nullable=False),
                    sa.Column('cumecs', sa.Integer(), nullable=False),
                    sa.Column('river_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['river_id'], ['rivers.id'],
                                            deferrable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_measures_river_id'), 'measures', ['river_id'],
                    unique=False)


def downgrade():
    op.drop_index(op.f('ix_measures_river_id'), table_name='measures')
    op.drop_table('measures')
    op.drop_table('rivers')
