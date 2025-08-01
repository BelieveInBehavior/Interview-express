"""Fix user model

Revision ID: c8ed562f65b1
Revises: 668a82073724
Create Date: 2025-07-06 11:12:41.535062

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c8ed562f65b1'
down_revision = '668a82073724'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.Integer(), nullable=False))
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50),
               nullable=False)
    op.drop_index('ix_users_phone', table_name='users')
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.create_index('ix_users_phone', 'users', ['phone'], unique=False)
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50),
               nullable=True)
    op.drop_column('users', 'id')
    # ### end Alembic commands ### 