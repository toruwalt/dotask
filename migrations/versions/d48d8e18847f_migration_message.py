"""migration_message

Revision ID: d48d8e18847f
Revises: 
Create Date: 2024-06-17 11:48:39.557601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd48d8e18847f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('username')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.VARCHAR(length=30), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.VARCHAR(length=30), nullable=False))
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=30), nullable=False))

    # ### end Alembic commands ###
