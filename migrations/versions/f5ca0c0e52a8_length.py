"""length

Revision ID: f5ca0c0e52a8
Revises: ad4d44d1029c
Create Date: 2019-03-10 02:17:35.455574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f5ca0c0e52a8'
down_revision = 'ad4d44d1029c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apply_record', sa.Column('project_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'apply_record_ibfk_3', 'apply_record', type_='foreignkey')
    op.create_foreign_key(None, 'apply_record', 'project', ['project_id'], ['id'])
    op.drop_column('apply_record', 'project')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apply_record', sa.Column('project', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'apply_record', type_='foreignkey')
    op.create_foreign_key(u'apply_record_ibfk_3', 'apply_record', 'project', ['project'], ['id'])
    op.drop_column('apply_record', 'project_id')
    # ### end Alembic commands ###
