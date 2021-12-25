"""correct published column to posts table

Revision ID: 27cdaf0512d9
Revises: 70c3a501df0a
Create Date: 2021-12-19 05:03:57.164646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27cdaf0512d9'
down_revision = '70c3a501df0a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass

def downgrade():
    op.drop_column('posts','published')
    pass
