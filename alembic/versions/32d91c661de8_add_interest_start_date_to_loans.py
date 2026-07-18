"""add interest_start_date to loans

Revision ID: 32d91c661de8
Revises: b16a6970d5ca
Create Date: 2026-07-18 16:39:57.433324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32d91c661de8"
down_revision: Union[str, Sequence[str], None] = "b16a6970d5ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Add column as nullable
    op.add_column(
        "loans",
        sa.Column(
            "interest_start_date",
            sa.Date(),
            nullable=True,
        ),
    )

    # Step 2: Copy issue_date into interest_start_date
    op.execute("""
        UPDATE loans
        SET interest_start_date = issue_date
    """)

    # Step 3: Make column NOT NULL
    op.alter_column(
        "loans",
        "interest_start_date",
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column("loans", "interest_start_date")