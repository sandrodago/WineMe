"""add social connections

Revision ID: 2b3c4d5e6f7a
Revises: 1a2b3c4d5e6f
Create Date: 2026-06-15 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2b3c4d5e6f7a"
down_revision: Union[str, None] = "1a2b3c4d5e6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "social_connections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("requester_id", sa.Integer(), nullable=False),
        sa.Column("addressee_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["requester_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["addressee_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("requester_id", "addressee_id", name="uq_social_connection_pair"),
    )
    op.create_index(op.f("ix_social_connections_id"), "social_connections", ["id"], unique=False)
    op.create_index(op.f("ix_social_connections_requester_id"), "social_connections", ["requester_id"], unique=False)
    op.create_index(op.f("ix_social_connections_addressee_id"), "social_connections", ["addressee_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_social_connections_addressee_id"), table_name="social_connections")
    op.drop_index(op.f("ix_social_connections_requester_id"), table_name="social_connections")
    op.drop_index(op.f("ix_social_connections_id"), table_name="social_connections")
    op.drop_table("social_connections")

