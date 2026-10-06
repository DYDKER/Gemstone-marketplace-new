"""Convert gemstone type to string

Revision ID: 56ad5f18ef5d
Revises: 7819bfd9dd29
Create Date: 2026-09-15 03:22:22.931415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '56ad5f18ef5d'
down_revision: Union[str, Sequence[str], None] = '7819bfd9dd29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('gemstones', 'gemstone_type',
               existing_type=postgresql.ENUM('DIAMOND', 'RUBY', 'SAPPHIRE', name='gemstone_type'),
               type_=sa.String(length=50),
               existing_nullable=False,
               postgresql_using="gemstone_type::text")
    # The old enum stored member names; the API uses their string values.
    op.execute("""
        UPDATE gemstones
        SET gemstone_type = CASE gemstone_type
            WHEN 'DIAMOND' THEN 'Diamond'
            WHEN 'RUBY' THEN 'Ruby'
            WHEN 'SAPPHIRE' THEN 'Sapphire'
            ELSE gemstone_type
        END
    """)
    postgresql.ENUM(name='gemstone_type').drop(op.get_bind())


def downgrade() -> None:
    """Downgrade schema."""
    gemstone_type = postgresql.ENUM(
        'DIAMOND', 'RUBY', 'SAPPHIRE', name='gemstone_type',
    )
    gemstone_type.create(op.get_bind())
    # Unknown new types intentionally fail the cast rather than lose data.
    op.alter_column('gemstones', 'gemstone_type',
               existing_type=sa.String(length=50),
               type_=gemstone_type,
               existing_nullable=False,
               postgresql_using="""(CASE gemstone_type
                   WHEN 'Diamond' THEN 'DIAMOND'
                   WHEN 'Ruby' THEN 'RUBY'
                   WHEN 'Sapphire' THEN 'SAPPHIRE'
                   ELSE gemstone_type
               END)::gemstone_type""")
