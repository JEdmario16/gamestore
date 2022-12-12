"""changes in user model

Revision ID: 701961916ea9
Revises: 6d4095b268d4
Create Date: 2022-12-10 11:35:51.617859

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '701961916ea9'
down_revision = '6d4095b268d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), nullable=False))
    op.drop_column('users', 'confirmed')
    op.drop_column('users', 'confirmed_on')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed_on', mysql.DATETIME(), nullable=True))
    op.add_column('users', sa.Column('confirmed', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('users', 'is_email_verified')
    # ### end Alembic commands ###