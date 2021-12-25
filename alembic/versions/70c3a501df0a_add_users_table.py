"""add users table

Revision ID: 70c3a501df0a
Revises: 4beff93bc7ad
Create Date: 2021-12-19 04:52:23.458240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70c3a501df0a'
down_revision = 'e8aeab81e532'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('name',sa.String(),nullable=False),
    sa.Column('email',sa.String(),nullable=False),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
              server_default=sa.text('now()',),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
