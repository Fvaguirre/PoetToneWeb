"""changed PoemTone and PoemFeature Models

Revision ID: 63dba0f9b46a
Revises: 69e61083cfe7
Create Date: 2018-12-07 01:04:25.877009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63dba0f9b46a'
down_revision = '69e61083cfe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('poem', sa.Column('times_liked', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('poem', 'times_liked')
    # ### end Alembic commands ###