"""empty message

Revision ID: 0ec32912a1dd
Revises: 96c4faf6f7cd
Create Date: 2023-07-13 22:31:58.706855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ec32912a1dd'
down_revision = '96c4faf6f7cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_association')
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('toy_id', sa.Integer(), nullable=False))
        batch_op.alter_column('reserve_status',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.create_foreign_key(None, 'toy', ['toy_id'], ['toy_id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('reserve_status',
               existing_type=sa.String(),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
        batch_op.drop_column('toy_id')
        batch_op.drop_column('user_id')

    op.create_table('transaction_association',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('toy_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['toy_id'], ['toy.toy_id'], name='transaction_association_toy_id_fkey'),
    sa.ForeignKeyConstraint(['transaction_id'], ['transaction.transaction_id'], name='transaction_association_transaction_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='transaction_association_user_id_fkey')
    )
    # ### end Alembic commands ###
