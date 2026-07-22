"""add_closed_at_to_loans"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "9ce77c91502d"
down_revision: Union[str, Sequence[str], None] = '32d91c661de8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add the closed_at column used to store
    when a loan is permanently closed.
    """

    op.add_column(
        "loans",
        sa.Column(
            "closed_at",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """
    Remove the closed_at column during rollback.
    """

    op.drop_column(
        "loans",
        "closed_at",
    )