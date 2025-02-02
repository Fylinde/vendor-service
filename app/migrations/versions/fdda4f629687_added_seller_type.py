"""Added seller Type

Revision ID: fdda4f629687
Revises: 835827ee47c3
Create Date: 2025-01-24 11:18:22.590232

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = "fdda4f629687"
down_revision = "835827ee47c3"
branch_labels = None
depends_on = None


def column_exists(connection, table_name, column_name):
    """Check if a column exists in the specified table."""
    inspector = Inspector.from_engine(connection)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    connection = op.get_bind()

    # Check if the 'seller_type' column exists before adding it
    if not column_exists(connection, "sellers", "seller_type"):
        # Add column with a default value for existing rows
        op.add_column(
            "sellers",
            sa.Column(
                "seller_type",
                sa.String(),
                nullable=False,
                server_default="default_type",
            ),
        )
        # Remove the default constraint after updating existing rows
        op.alter_column("sellers", "seller_type", server_default=None)
        print("Added column 'seller_type' to 'sellers'.")
    else:
        print("Column 'seller_type' already exists in 'sellers'. Skipping addition.")


def downgrade():
    connection = op.get_bind()

    # Check if the 'seller_type' column exists before dropping it
    if column_exists(connection, "sellers", "seller_type"):
        op.drop_column("sellers", "seller_type")
        print("Dropped column 'seller_type' from 'sellers'.")
    else:
        print("Column 'seller_type' does not exist in 'sellers'. Skipping drop.")
