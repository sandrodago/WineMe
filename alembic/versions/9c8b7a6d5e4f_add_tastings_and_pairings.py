"""add tastings and pairings

Revision ID: 9c8b7a6d5e4f
Revises: a1b2c3d4e5f6
Create Date: 2026-06-15 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9c8b7a6d5e4f"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tastings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("wine_id", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["wine_id"], ["wines.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tastings_id"), "tastings", ["id"], unique=False)
    op.create_index(op.f("ix_tastings_user_id"), "tastings", ["user_id"], unique=False)
    op.create_index(op.f("ix_tastings_wine_id"), "tastings", ["wine_id"], unique=False)

    op.create_table(
        "pairings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("wine_id", sa.Integer(), nullable=False),
        sa.Column("food", sa.String(), nullable=False),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["wine_id"], ["wines.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pairings_id"), "pairings", ["id"], unique=False)
    op.create_index(op.f("ix_pairings_user_id"), "pairings", ["user_id"], unique=False)
    op.create_index(op.f("ix_pairings_wine_id"), "pairings", ["wine_id"], unique=False)
    op.create_index(op.f("ix_pairings_food"), "pairings", ["food"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_pairings_food"), table_name="pairings")
    op.drop_index(op.f("ix_pairings_wine_id"), table_name="pairings")
    op.drop_index(op.f("ix_pairings_user_id"), table_name="pairings")
    op.drop_index(op.f("ix_pairings_id"), table_name="pairings")
    op.drop_table("pairings")

    op.drop_index(op.f("ix_tastings_wine_id"), table_name="tastings")
    op.drop_index(op.f("ix_tastings_user_id"), table_name="tastings")
    op.drop_index(op.f("ix_tastings_id"), table_name="tastings")
    op.drop_table("tastings")

