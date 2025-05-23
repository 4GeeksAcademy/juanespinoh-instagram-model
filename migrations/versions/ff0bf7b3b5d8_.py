"""empty message

Revision ID: ff0bf7b3b5d8
Revises: a5cffa318ac2
Create Date: 2025-04-16 16:29:27.420224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff0bf7b3b5d8'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('bio', sa.String(length=300), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bio')
        batch_op.drop_column('user_name')

    op.drop_table('post')
    # ### end Alembic commands ###
