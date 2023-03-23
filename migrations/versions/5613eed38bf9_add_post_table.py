"""Add post table

Revision ID: 5613eed38bf9
Revises: 0418290e0ef8
Create Date: 2023-03-23 14:25:44.999819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5613eed38bf9'
down_revision = '0418290e0ef8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('image_url', sa.String(length=100), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
