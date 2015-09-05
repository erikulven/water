"""add sjoa river

Revision ID: 39e47a013b5
Revises: 132e1596946
Create Date: 2015-09-05 17:31:18.824393

"""

# revision identifiers, used by Alembic.
revision = '39e47a013b5'
down_revision = '132e1596946'

from datetime import datetime
from sqlalchemy.sql import table, column
from alembic import op
import sqlalchemy as sa


def upgrade():
    rivers_table = table('rivers',
                         column('id', sa.Integer),
                         column('identifier', sa.String),
                         column('source', sa.String),
                         column('name', sa.String),
                         column('created_at', sa.DateTime),
                         column('updated_at', sa.DateTime))
    op.bulk_insert(
        rivers_table,
        [
           {
                'id': 19,
                'identifier': '0002.00595.000',
                'source': 'NVE',
                'name': 'Sjoa-Faukstad',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
        ],
    )


def downgrade():
    pass
