"""Added is_approved

Revision ID: a08bbf6ab15e
Revises: 8adf3b0b1abe
Create Date: 2024-11-10 13:56:26.171050

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision = "a08bbf6ab15e"
down_revision = "8adf3b0b1abe"
branch_labels = None
depends_on = None


def upgrade():
    # Reflect the current table structure
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)
    columns = [column["name"] for column in inspector.get_columns("sellers")]

    # Add 'is_approved' column
    if "is_approved" not in columns:
        op.add_column("sellers", sa.Column("is_approved", sa.Boolean(), nullable=True))

    # Add 'first_name', 'middle_name', and 'last_name' columns if they do not exist
    if "first_name" not in columns:
        op.add_column(
            "sellers", sa.Column("first_name", sa.VARCHAR(length=128), nullable=True)
        )
    if "middle_name" not in columns:
        op.add_column(
            "sellers", sa.Column("middle_name", sa.VARCHAR(length=128), nullable=True)
        )
    if "last_name" not in columns:
        op.add_column(
            "sellers", sa.Column("last_name", sa.VARCHAR(length=128), nullable=True)
        )


def downgrade():
    # Reflect the current table structure
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)
    columns = [column["name"] for column in inspector.get_columns("sellers")]

    # Drop 'is_approved' column if it exists
    if "is_approved" in columns:
        op.drop_column("sellers", "is_approved")

    # Drop 'first_name', 'middle_name', and 'last_name' columns if they exist
    if "first_name" in columns:
        op.drop_column("sellers", "first_name")
    if "middle_name" in columns:
        op.drop_column("sellers", "middle_name")
    if "last_name" in columns:
        op.drop_column("sellers", "last_name")
