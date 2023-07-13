"""empty message

Revision ID: cd9fca80027f
Revises: 8ece236caf02
Create Date: 2023-07-13 10:54:50.797121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd9fca80027f'
down_revision = '8ece236caf02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('toy', schema=None) as batch_op:
        batch_op.add_column(sa.Column('toy_hold_number', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('toy', schema=None) as batch_op:
        batch_op.drop_column('toy_hold_number')

    # ### end Alembic commands ###
