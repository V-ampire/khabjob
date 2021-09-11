"""Add users table

Revision ID: 857846dd0650
Revises: db3d36046856
Create Date: 2021-09-07 22:39:09.028993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '857846dd0650'
down_revision = 'db3d36046856'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('password_hash'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###