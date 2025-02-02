"""Add new models

Revision ID: 5486d8d52683
Revises: a08bbf6ab15e
Create Date: 2025-01-08 08:30:09.541147

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# Revision identifiers, used by Alembic.
revision = "5486d8d52683"
down_revision = "a08bbf6ab15e"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    # Drop 'vendors' table if it exists
    if "vendors" in inspector.get_table_names():
        if "ix_vendors_email" in [index["name"] for index in inspector.get_indexes("vendors")]:
            op.drop_index("ix_vendors_email", table_name="vendors")
        if "ix_vendors_id" in [index["name"] for index in inspector.get_indexes("vendors")]:
            op.drop_index("ix_vendors_id", table_name="vendors")
        op.drop_table("vendors")

    # Create 'sellers' table
    if "sellers" not in inspector.get_table_names():
        op.create_table(
            "sellers",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("full_name", sa.String(length=255), nullable=False),
            sa.Column("email", sa.String(), nullable=False, unique=True),
            sa.Column("hashed_password", sa.String(), nullable=False),
            sa.Column("phoneNumber", sa.String(length=20), nullable=True),
            sa.Column("profile_picture", sa.String(), nullable=True),
            sa.Column("current_step", sa.String(length=50), nullable=True),
            sa.Column("registration_data", sa.JSON(), nullable=True),
            sa.Column("verification_code", sa.String(), nullable=True),
            sa.Column("verification_expiration", sa.DateTime(), nullable=True),
            sa.Column("preferences", sa.JSON(), nullable=True),
            sa.Column("notification_preferences", sa.String(), nullable=True),
            sa.Column("language_code", sa.String(length=35), nullable=True),
            sa.Column("currency_code", sa.String(length=10), nullable=True),
            sa.Column("ai_recommendation_opt_in", sa.Boolean(), nullable=True),
            sa.Column("two_factor_enabled", sa.Boolean(), nullable=True),
            sa.Column("two_factor_secret", sa.String(), nullable=True),
            sa.Column("notifications_enabled", sa.Boolean(), nullable=True),
            sa.Column("is_email_verified", sa.Boolean(), nullable=True),
            sa.Column("is_phone_verified", sa.Boolean(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=True),
            sa.Column("is_admin", sa.Boolean(), nullable=True),
            sa.Column("is_approved", sa.Boolean(), nullable=True),
            sa.Column("escrow_balance", sa.Float(), nullable=True),
            sa.Column("password_last_updated", sa.DateTime(), nullable=True),
            sa.Column("date_of_birth", sa.String(), nullable=True),
            sa.Column("gender", sa.String(length=10), nullable=True),
            sa.Column("last_login", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.Column("jwt_token_key", sa.String(), nullable=True),
            sa.Column("exchange_rates", sa.JSON(), nullable=True),
        )
        op.create_index("ix_sellers_email", "sellers", ["email"], unique=True)
        op.create_index("ix_sellers_id", "sellers", ["id"])

    # Create 'live_shopping_sessions' table
    if "live_shopping_sessions" not in inspector.get_table_names():
        op.create_table(
            "live_shopping_sessions",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("sellerId", sa.Integer(), sa.ForeignKey("sellers.id"), nullable=False),
            sa.Column("session_details", sa.JSON(), nullable=False),
            sa.Column("started_at", sa.DateTime(), nullable=True),
            sa.Column("ended_at", sa.DateTime(), nullable=True),
        )
        op.create_index(
            "ix_live_shopping_sessions_id", "live_shopping_sessions", ["id"], unique=False
        )

    # Create 'seller_ratings' table
    if "seller_ratings" not in inspector.get_table_names():
        op.create_table(
            "seller_ratings",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("sellerId", sa.Integer(), sa.ForeignKey("sellers.id"), nullable=False),
            sa.Column("rating", sa.Float(), nullable=False),
            sa.Column("review", sa.String(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
        )
        op.create_index("ix_seller_ratings_id", "seller_ratings", ["id"], unique=False)

    # Create 'seller_transactions' table
    if "seller_transactions" not in inspector.get_table_names():
        op.create_table(
            "seller_transactions",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("sellerId", sa.Integer(), sa.ForeignKey("sellers.id"), nullable=False),
            sa.Column("transaction_type", sa.String(), nullable=False),
            sa.Column("amount", sa.Float(), nullable=False),
            sa.Column("status", sa.String(), nullable=False, default="pending"),
            sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        )
        op.create_index("ix_seller_transactions_id", "seller_transactions", ["id"], unique=False)


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    # Drop 'seller_transactions' table
    if "seller_transactions" in inspector.get_table_names():
        op.drop_index("ix_seller_transactions_id", table_name="seller_transactions")
        op.drop_table("seller_transactions")

    # Drop 'seller_ratings' table
    if "seller_ratings" in inspector.get_table_names():
        op.drop_index("ix_seller_ratings_id", table_name="seller_ratings")
        op.drop_table("seller_ratings")

    # Drop 'live_shopping_sessions' table
    if "live_shopping_sessions" in inspector.get_table_names():
        op.drop_index("ix_live_shopping_sessions_id", table_name="live_shopping_sessions")
        op.drop_table("live_shopping_sessions")

    # Drop 'sellers' table
    if "sellers" in inspector.get_table_names():
        op.drop_index("ix_sellers_email", table_name="sellers")
        op.drop_index("ix_sellers_id", table_name="sellers")
        op.drop_table("sellers")

    # Recreate 'vendors' table
    if "vendors" not in inspector.get_table_names():
        op.create_table(
            "vendors",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            # Add other columns as needed...
        )
