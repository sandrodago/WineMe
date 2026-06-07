"""create cellar entries table

Revision ID: a1b2c3d4e5f6
Revises: f118559ed3a0
Create Date: 2026-06-06 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "f118559ed3a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cellar_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("wine_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["wine_id"], ["wines.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "wine_id", name="uq_user_wine"),
    )
    op.create_index(op.f("ix_cellar_entries_id"), "cellar_entries", ["id"], unique=False)
    op.create_index(op.f("ix_cellar_entries_user_id"), "cellar_entries", ["user_id"], unique=False)
    op.create_index(op.f("ix_cellar_entries_wine_id"), "cellar_entries", ["wine_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cellar_entries_wine_id"), table_name="cellar_entries")
    op.drop_index(op.f("ix_cellar_entries_user_id"), table_name="cellar_entries")
    op.drop_index(op.f("ix_cellar_entries_id"), table_name="cellar_entries")
    op.drop_table("cellar_entries")
