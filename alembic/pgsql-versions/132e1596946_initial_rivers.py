"""initial rivers

Revision ID: 132e1596946
Revises: 1499a13be24
Create Date: 2015-06-20 09:27:34.931805

"""

# revision identifiers, used by Alembic.
from datetime import datetime

revision = '132e1596946'
down_revision = '1499a13be24'

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
                'id': 1,
                'identifier': 'Losna',
                'source': 'GLB',
                'name': 'Losna',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 2,
                'identifier': '0002.00145.000',
                'source': 'NVE',
                'name': 'Losna (nve)',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 3,
                'identifier': '0012.00070.000',
                'source': 'NVE',
                'name': 'Etna',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 4,
                'identifier': 'Frya',
                'source': 'GLB',
                'name': 'Frya',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 5,
                'identifier': '0002.00063.000',
                'source': 'NVE',
                'name': 'Frya (nve)',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 6,
                'identifier': 'Rosten',
                'source': 'GLB',
                'name': 'Rosten',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 7,
                'identifier': 'Faukstad (Sjoa)',
                'source': 'GLB',
                'name': 'Sjoa',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 8,
                'identifier': 'Gausa',
                'source': 'GLB',
                'name': 'Gausa',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 9,
                'identifier': '0002.00028.000',
                'source': 'NVE',
                'name': 'Gausa (nve)',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 10,
                'identifier': '0002.00303.000',
                'source': 'NVE',
                'name': 'Jori',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 11,
                'identifier': '0103.00003.000',
                'source': 'NVE',
                'name': 'Upper Rauma',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 12,
                'identifier': '0002.00032.000',
                'source': 'NVE',
                'name': 'Atnasj.',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 13,
                'identifier': '0012.00209.000',
                'source': 'NVE',
                'name': 'Urula',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 14,
                'identifier': '0002.00463.000',
                'source': 'NVE',
                'name': 'Vismunda',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 15,
                'identifier': '0002.00578.000',
                'source': 'NVE',
                'name': 'Imsa',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 16,
                'identifier': '0002.00439.000',
                'source': 'NVE',
                'name': 'Aasta',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 17,
                'identifier': '0002.00267.000',
                'source': 'NVE',
                'name': 'Mistra',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 18,
                'identifier': '0002.00290.000',
                'source': 'NVE',
                'name': 'Bovra',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
        ],
    )


def downgrade():
    rivers_table = table('rivers')
    op.execute(
        rivers_table.delete())
