""".

Revision ID: 5fe72b1a073b
Revises: 83f5b0df3839
Create Date: 2018-11-08 02:28:25.200986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fe72b1a073b'
down_revision = '83f5b0df3839'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('data_catin', 'is_public',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('data_catin', 'is_public',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
