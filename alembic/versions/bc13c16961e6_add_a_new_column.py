"""Add a new column

Revision ID: bc13c16961e6
Revises: 2c601100a50e
Create Date: 2023-02-19 12:16:32.250054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc13c16961e6'
down_revision = '2c601100a50e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
