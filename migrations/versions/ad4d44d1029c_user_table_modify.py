"""user table modify

Revision ID: ad4d44d1029c
Revises: 
Create Date: 2019-03-07 12:12:54.526805

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ad4d44d1029c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('account', sa.String(length=20), nullable=False))
    op.add_column('user', sa.Column('department_id', sa.Integer(), nullable=True))
    op.alter_column('user', 'class_name',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    op.create_foreign_key(None, 'user', 'audit_department', ['department_id'], ['id'])
    op.drop_column('user', 'stu_num')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('stu_num', mysql.VARCHAR(length=20), nullable=False))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.alter_column('user', 'class_name',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    op.drop_column('user', 'department_id')
    op.drop_column('user', 'account')
    # ### end Alembic commands ###
