"""sauce2

Revision ID: d684a20c16e2
Revises: f44cf2b4a069
Create Date: 2024-07-01 19:08:35.356762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd684a20c16e2'
down_revision = 'f44cf2b4a069'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pizza_type_sauce_quantity',
    sa.Column('pizza_type_id', sa.Uuid(), nullable=False),
    sa.Column('sauce_id', sa.Uuid(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pizza_type_id'], ['pizza_type.id'], ),
    sa.ForeignKeyConstraint(['sauce_id'], ['sauces.id'], ),
    sa.PrimaryKeyConstraint('pizza_type_id', 'sauce_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pizza_type_sauce_quantity')
    # ### end Alembic commands ###
