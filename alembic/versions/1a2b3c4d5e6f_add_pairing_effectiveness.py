"""add pairing effectiveness

Revision ID: 1a2b3c4d5e6f
Revises: 9c8b7a6d5e4f
Create Date: 2026-06-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1a2b3c4d5e6f"
down_revision: Union[str, None] = "9c8b7a6d5e4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "pairings",
        sa.Column("effectiveness", sa.Integer(), nullable=False, server_default="3"),
    )
    op.alter_column("pairings", "effectiveness", server_default=None)


def downgrade() -> None:
    op.drop_column("pairings", "effectiveness")

