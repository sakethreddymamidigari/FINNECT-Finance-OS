"""initial schema

Revision ID: d6ac1a52b66e
Revises:
Create Date: 2026-07-18 15:36:51.276106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d6ac1a52b66e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "loans",
        sa.Column(
            "remaining_principal",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
            server_default="0",
        ),
    )

    op.add_column(
        "loans",
        sa.Column(
            "total_principal_paid",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
        ),
    )

    op.add_column(
        "loans",
        sa.Column(
            "total_interest_paid",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
        ),
    )

    op.add_column(
        "loans",
        sa.Column(
            "last_interest_calculated_on",
            sa.Date(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("loans", "last_interest_calculated_on")
    op.drop_column("loans", "total_interest_paid")
    op.drop_column("loans", "total_principal_paid")
    op.drop_column("loans", "remaining_principal")