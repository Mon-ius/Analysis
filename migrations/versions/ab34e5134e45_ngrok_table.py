"""ngrok table

Revision ID: ab34e5134e45
Revises: 
Create Date: 2018-05-12 10:38:22.831681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab34e5134e45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ngrok',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pub', sa.String(length=128), nullable=True),
    sa.Column('loc', sa.String(length=128), nullable=True),
    sa.Column('time', sa.String(length=120), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ngrok_pub'), 'ngrok', ['pub'], unique=True)
    op.create_index(op.f('ix_ngrok_time'), 'ngrok', ['time'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ngrok_time'), table_name='ngrok')
    op.drop_index(op.f('ix_ngrok_pub'), table_name='ngrok')
    op.drop_table('ngrok')
    # ### end Alembic commands ###