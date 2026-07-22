"""create finance settings table

Revision ID: cfd3cf3575ae
Revises: 9ce77c91502d
Create Date: 2026-07-22 18:39:31.976642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfd3cf3575ae'
down_revision: Union[str, Sequence[str], None] = '9ce77c91502d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "finance_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("finance_owner_id", sa.Integer(), nullable=False),
        sa.Column("business_name", sa.String(length=150), nullable=True),
        sa.Column("owner_name", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("address", sa.String(length=300), nullable=True),
        sa.Column("default_interest_method", sa.String(length=20), nullable=False),
        sa.Column("default_interest_rate", sa.Numeric(10, 2), nullable=False),
        sa.Column("default_loan_duration", sa.Integer(), nullable=False),
        sa.Column("default_grace_period", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("date_format", sa.String(length=20), nullable=False),
        sa.Column("timezone", sa.String(length=50), nullable=False),
        sa.Column("maturity_alert_days", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["finance_owner_id"],
            ["finance_owners.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("finance_owner_id"),
    )

    op.create_index(
        op.f("ix_finance_settings_id"),
        "finance_settings",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_finance_settings_finance_owner_id"),
        "finance_settings",
        ["finance_owner_id"],
        unique=True,
    )

def downgrade() -> None:
    op.drop_index(
        op.f("ix_finance_settings_finance_owner_id"),
        table_name="finance_settings",
    )

    op.drop_index(
        op.f("ix_finance_settings_id"),
        table_name="finance_settings",
    )

    op.drop_table("finance_settings")
