"""empty message

Revision ID: 2b4c61eb00af
Revises: c220e24edc3d
Create Date: 2023-08-02 15:05:16.799330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b4c61eb00af'
down_revision = 'c220e24edc3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firebase_uid', sa.Integer(), nullable=False))
        batch_op.drop_constraint('transaction_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['firebase_uid'], ['firebase_uid'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('transaction_user_id_fkey', 'user', ['user_id'], ['user_id'])
        batch_op.drop_column('firebase_uid')

    # ### end Alembic commands ###
