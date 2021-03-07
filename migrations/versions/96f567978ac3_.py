"""empty message

Revision ID: 96f567978ac3
Revises: 367eaf38be7f
Create Date: 2021-03-07 03:29:27.098393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96f567978ac3'
down_revision = '367eaf38be7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transfer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.Integer(), nullable=False),
    sa.Column('receiver', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.Column('memo', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(), server_default='PENDING', nullable=False),
    sa.Column('opened_on', sa.DateTime(), nullable=False),
    sa.Column('closed_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['receiver'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('transfers')
    op.add_column('user', sa.Column('allowance', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('balance', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'balance')
    op.drop_column('user', 'allowance')
    op.create_table('transfers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sender', sa.INTEGER(), nullable=True),
    sa.Column('receiver', sa.INTEGER(), nullable=True),
    sa.Column('value', sa.INTEGER(), nullable=True),
    sa.Column('memo', sa.VARCHAR(length=100), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('opened_on', sa.DATETIME(), nullable=True),
    sa.Column('closed_on', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['receiver'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('transfer')
    # ### end Alembic commands ###
