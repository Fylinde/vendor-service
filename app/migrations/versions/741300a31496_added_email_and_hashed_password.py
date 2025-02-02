"""Added email and hashed_password

Revision ID: 741300a31496
Revises: f5bd624da99f
Create Date: 2024-10-30 09:43:35.067438

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '741300a31496'
down_revision = 'f5bd624da99f'
branch_labels = None
depends_on = None


def column_exists(connection, table_name, column_name):
    """Check if a column exists in a table."""
    inspector = Inspector.from_engine(connection)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    connection = op.get_bind()

    # Check if 'email' column exists before adding it
    if not column_exists(connection, "sellers", "email"):
        op.add_column('sellers', sa.Column('email', sa.String(), nullable=False))
        op.create_index(op.f('ix_sellers_email'), 'sellers', ['email'], unique=True)
        print("Added column 'email' to 'sellers' and created index.")
    else:
        print("Column 'email' already exists in 'sellers'. Skipping.")

    # Check if 'hashed_password' column exists before adding it
    if not column_exists(connection, "sellers", "hashed_password"):
        op.add_column('sellers', sa.Column('hashed_password', sa.String(), nullable=False))
        print("Added column 'hashed_password' to 'sellers'.")
    else:
        print("Column 'hashed_password' already exists in 'sellers'. Skipping.")


def downgrade():
    connection = op.get_bind()

    # Check if 'email' column exists before dropping it
    if column_exists(connection, "sellers", "email"):
        op.drop_index(op.f('ix_sellers_email'), table_name='sellers')
        op.drop_column('sellers', 'email')
        print("Dropped column 'email' from 'sellers'.")
    else:
        print("Column 'email' does not exist in 'sellers'. Skipping drop.")

    # Check if 'hashed_password' column exists before dropping it
    if column_exists(connection, "sellers", "hashed_password"):
        op.drop_column('sellers', 'hashed_password')
        print("Dropped column 'hashed_password' from 'sellers'.")
    else:
        print("Column 'hashed_password' does not exist in 'sellers'. Skipping drop.")
