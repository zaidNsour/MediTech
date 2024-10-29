"""modify notification

Revision ID: 1f18d0659f63
Revises: 672dce9b03bd
Create Date: 2024-10-29 13:54:49.730812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f18d0659f63'
down_revision = '672dce9b03bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('status', sa.String(length=80), nullable=False))
        batch_op.drop_column('message')
        batch_op.drop_column('title')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('message', sa.TEXT(), nullable=False))
        batch_op.drop_column('status')
        batch_op.drop_column('content')

    # ### end Alembic commands ###
