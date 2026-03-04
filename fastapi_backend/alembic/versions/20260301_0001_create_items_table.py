"""create items table

Revision ID: 20260301_0001
Revises:
Create Date: 2026-03-01 15:15:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260301_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sku", sa.String(length=64), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_items_id", "items", ["id"], unique=False)
    op.create_index("ix_items_name", "items", ["name"], unique=False)
    op.create_index("ix_items_sku", "items", ["sku"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_items_sku", table_name="items")
    op.drop_index("ix_items_name", table_name="items")
    op.drop_index("ix_items_id", table_name="items")
    op.drop_table("items")
