"""create gemstones table

Revision ID: 13d24869a682
Revises: 0dd511b33ade
Create Date: 2026-09-03 00:21:41.256402

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "13d24869a682"
down_revision: str | Sequence[str] | None = "0dd511b33ade"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "gemstones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=240), nullable=False),
        sa.Column("gemstone_type", sa.String(length=50), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("carat_weight", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=320), nullable=True),
        sa.Column(
            "is_available",
            sa.Boolean(),
            server_default=sa.true(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("gemstones")
