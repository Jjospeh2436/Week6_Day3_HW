"""added weapon table

Revision ID: 07362d8682d1
Revises: 98ad39fa2040
Create Date: 2023-11-16 17:48:28.771545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07362d8682d1'
down_revision = '98ad39fa2040'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weapons',
    sa.Column('weap_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('weap_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weapons')
    # ### end Alembic commands ###
