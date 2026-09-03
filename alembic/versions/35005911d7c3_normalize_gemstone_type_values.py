"""normalize gemstone type values

Revision ID: 35005911d7c3
Revises: 5cb0bc6abcbe
Create Date: 2026-09-03 21:56:56.141472

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "35005911d7c3"
down_revision: str | Sequence[str] | None = "5cb0bc6abcbe"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        sa.text(
            """
            UPDATE gemstones
            SET gemstone_type = CASE gemstone_type
                WHEN 'DIAMOND' THEN 'Diamond'
                WHEN 'RUBY' THEN 'Ruby'
                WHEN 'SAPPHIRE' THEN 'Sapphire'
            END
            WHERE gemstone_type IN ('DIAMOND', 'RUBY', 'SAPPHIRE')
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            """
            UPDATE gemstones
            SET gemstone_type = CASE gemstone_type
                WHEN 'Diamond' THEN 'DIAMOND'
                WHEN 'Ruby' THEN 'RUBY'
                WHEN 'Sapphire' THEN 'SAPPHIRE'
            END
            WHERE gemstone_type IN ('Diamond', 'Ruby', 'Sapphire')
            """
        )
    )
