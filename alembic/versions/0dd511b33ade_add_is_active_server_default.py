"""add is active server default

Revision ID: 0dd511b33ade
Revises: 714865f5b46d
Create Date: 2026-08-27 07:56:33.611119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dd511b33ade'
down_revision: Union[str, Sequence[str], None] = '714865f5b46d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "is_active",
        existing_type=sa.Boolean(),
        server_default=sa.true(),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "is_active",
        existing_type=sa.Boolean(),
        server_default=None,
    )
