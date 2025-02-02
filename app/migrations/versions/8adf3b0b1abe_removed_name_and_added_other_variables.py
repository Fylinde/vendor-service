"""Removed name and added other variables

Revision ID: 8adf3b0b1abe
Revises: 741300a31496
Create Date: 2024-10-30 11:17:18.676831

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "8adf3b0b1abe"
down_revision = "741300a31496"
branch_labels = None
depends_on = None


def column_exists(connection, table_name, column_name):
    """Check if a column exists in a table."""
    inspector = Inspector.from_engine(connection)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    connection = op.get_bind()

    # Check and add columns if they do not already exist
    columns_to_add = [
        ("full_name", sa.String(length=255), False),
        ("first_name", sa.String(length=128), True),
        ("middle_name", sa.String(length=128), True),
        ("last_name", sa.String(length=128), True),
        ("phoneNumber", sa.String(length=20), True),
        ("profile_picture", sa.String(), True),
        ("jwt_token_key", sa.String(), True),
        ("password_last_updated", sa.DateTime(), True),
        ("preferences", sa.JSON(), True),
        ("notification_preferences", sa.String(), True),
        ("verification_expiration", sa.DateTime(), True),
        ("language_code", sa.String(length=35), True),
        ("is_admin", sa.Boolean(), True),
        ("verification_code", sa.String(), True),
        ("date_of_birth", sa.String(), True),
        ("gender", sa.String(length=10), True),
        ("is_email_verified", sa.Boolean(), True),
        ("is_phone_verified", sa.Boolean(), True),
        ("two_factor_enabled", sa.Boolean(), True),
        ("two_factor_secret", sa.String(), True),
        ("notifications_enabled", sa.Boolean(), True),
        ("ai_recommendation_opt_in", sa.Boolean(), True),
    ]

    for column_name, column_type, nullable in columns_to_add:
        if not column_exists(connection, "sellers", column_name):
            op.add_column(
                "sellers", sa.Column(column_name, column_type, nullable=nullable)
            )
            print(f"Added column '{column_name}' to 'sellers'.")
        else:
            print(f"Column '{column_name}' already exists in 'sellers'. Skipping.")

    # Alter column with explicit casting to boolean using the USING clause
    if column_exists(connection, "sellers", "is_active"):
        op.alter_column(
            "sellers",
            "is_active",
            existing_type=sa.VARCHAR(),
            type_=sa.Boolean(),
            existing_nullable=True,
            postgresql_using="is_active::boolean",
        )
        print("Altered column 'is_active' to Boolean.")

    # Check and drop the `name` column if it exists
    if column_exists(connection, "sellers", "name"):
        op.drop_index("ix_sellers_name", table_name="sellers")
        op.drop_column("sellers", "name")
        print("Dropped column 'name' from 'sellers'.")


def downgrade():
    connection = op.get_bind()

    # Re-add the `name` column if it doesn't exist
    if not column_exists(connection, "sellers", "name"):
        op.add_column(
            "sellers", sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True)
        )
        op.create_index("ix_sellers_name", "sellers", ["name"], unique=False)
        print("Re-added column 'name' to 'sellers'.")

    # Reverse the changes made during the upgrade
    columns_to_remove = [
        "ai_recommendation_opt_in",
        "notifications_enabled",
        "two_factor_secret",
        "two_factor_enabled",
        "is_phone_verified",
        "is_email_verified",
        "gender",
        "date_of_birth",
        "verification_code",
        "is_admin",
        "language_code",
        "verification_expiration",
        "notification_preferences",
        "preferences",
        "password_last_updated",
        "jwt_token_key",
        "profile_picture",
        "phoneNumber",
        "last_name",
        "middle_name",
        "first_name",
        "full_name",
    ]

    for column_name in columns_to_remove:
        if column_exists(connection, "sellers", column_name):
            op.drop_column("sellers", column_name)
            print(f"Dropped column '{column_name}' from 'sellers'.")
        else:
            print(f"Column '{column_name}' does not exist in 'sellers'. Skipping drop.")

    # Revert the `is_active` column alteration
    if column_exists(connection, "sellers", "is_active"):
        op.alter_column(
            "sellers",
            "is_active",
            existing_type=sa.Boolean(),
            type_=sa.VARCHAR(),
            existing_nullable=True,
        )
        print("Reverted column 'is_active' to VARCHAR.")
