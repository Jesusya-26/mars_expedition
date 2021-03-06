"""Добавили родной город пользователя

Revision ID: f19cebcdf35d
Revises: db8b24f52b6f
Create Date: 2022-03-05 23:34:15.048207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f19cebcdf35d'
down_revision = 'db8b24f52b6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('city_from', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'city_from')
    # ### end Alembic commands ###
