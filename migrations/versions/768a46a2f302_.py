"""empty message

Revision ID: 768a46a2f302
Revises: 89401030d219
Create Date: 2023-07-11 20:59:05.347474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '768a46a2f302'
down_revision = '89401030d219'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('toy', schema=None) as batch_op:
        batch_op.add_column(sa.Column('checked_out_by_user', sa.Integer(), nullable=True))
        batch_op.drop_constraint('toy_checked_out_by_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['checked_out_by_user'], ['user_id'])
        batch_op.drop_column('checked_out_by_user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('toy', schema=None) as batch_op:
        batch_op.add_column(sa.Column('checked_out_by_user_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('toy_checked_out_by_user_id_fkey', 'user', ['checked_out_by_user_id'], ['user_id'])
        batch_op.drop_column('checked_out_by_user')

    # ### end Alembic commands ###
