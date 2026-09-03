"""add user password hash

Revision ID: 5e34e1d301a6
Revises: 35005911d7c3
Create Date: 2026-09-03 22:08:16.119982

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5e34e1d301a6"
down_revision: str | Sequence[str] | None = "35005911d7c3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE users SET hashed_password = '!unusable-password!' "
            "WHERE hashed_password IS NULL"
        )
    )
    op.alter_column("users", "hashed_password", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "hashed_password")
