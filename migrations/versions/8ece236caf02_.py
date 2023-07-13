"""empty message

Revision ID: 8ece236caf02
Revises: a83475e3bab9
Create Date: 2023-07-13 00:11:01.851866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ece236caf02'
down_revision = 'a83475e3bab9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('check_out_history',
    sa.Column('checkout_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('toy_id', sa.Integer(), nullable=False),
    sa.Column('check_out_date', sa.Date(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('return_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['toy_id'], ['toy.toy_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('checkout_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('check_out_history')
    # ### end Alembic commands ###
