"""Add missing columns to sellers table

Revision ID: 6b3f585288d7
Revises: 5486d8d52683
Create Date: 2025-01-12 20:38:41.547335

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "6b3f585288d7"
down_revision = "5486d8d52683"
branch_labels = None
depends_on = None


def column_exists(connection, table_name, column_name):
    """Check if a column exists in a table."""
    inspector = Inspector.from_engine(connection)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    connection = op.get_bind()

    # Alter 'seller_transactions' column
    op.alter_column(
        "seller_transactions",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )

    # List of columns to add with their types and nullable flags
    columns_to_add = [
        ("current_step", sa.String(length=50), True),
        ("registration_data", sa.JSON(), True),
        ("currency_code", sa.String(length=10), True),
        ("escrow_balance", sa.Float(), True),
        ("last_login", sa.DateTime(), True),
        ("created_at", sa.DateTime(), False),
        ("updated_at", sa.DateTime(), True),
        ("exchange_rates", sa.JSON(), True),
    ]

    for column_name, column_type, nullable in columns_to_add:
        if not column_exists(connection, "sellers", column_name):
            op.add_column("sellers", sa.Column(column_name, column_type, nullable=nullable))
            print(f"Added column '{column_name}' to 'sellers'.")
        else:
            print(f"Column '{column_name}' already exists in 'sellers'. Skipping.")

    # Columns to drop from the `sellers` table
    columns_to_drop = ["last_name", "description", "middle_name", "first_name"]
    for column_name in columns_to_drop:
        if column_exists(connection, "sellers", column_name):
            op.drop_column("sellers", column_name)
            print(f"Dropped column '{column_name}' from 'sellers'.")
        else:
            print(f"Column '{column_name}' does not exist in 'sellers'. Skipping.")


def downgrade():
    connection = op.get_bind()

    # Add back the dropped columns if not already present
    columns_to_add_back = [
        ("first_name", sa.VARCHAR(length=128), True),
        ("middle_name", sa.VARCHAR(length=128), True),
        ("description", sa.VARCHAR(), True),
        ("last_name", sa.VARCHAR(length=128), True),
    ]
    for column_name, column_type, nullable in columns_to_add_back:
        if not column_exists(connection, "sellers", column_name):
            op.add_column("sellers", sa.Column(column_name, column_type, nullable=nullable))
            print(f"Re-added column '{column_name}' to 'sellers'.")
        else:
            print(f"Column '{column_name}' already exists in 'sellers'. Skipping re-addition.")

    # Drop the added columns
    columns_to_remove = [
        "exchange_rates",
        "updated_at",
        "created_at",
        "last_login",
        "escrow_balance",
        "currency_code",
        "registration_data",
        "current_step",
    ]
    for column_name in columns_to_remove:
        if column_exists(connection, "sellers", column_name):
            op.drop_column("sellers", column_name)
            print(f"Dropped column '{column_name}' from 'sellers'.")
        else:
            print(f"Column '{column_name}' does not exist in 'sellers'. Skipping drop.")

    # Revert the alteration on 'seller_transactions'
    op.alter_column(
        "seller_transactions",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    print("Reverted 'created_at' column alteration in 'seller_transactions'.")
