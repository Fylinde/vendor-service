"""Added lastActivityTimestamp

Revision ID: 835827ee47c3
Revises: 6b3f585288d7
Create Date: 2025-01-16 08:38:10.717473

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '835827ee47c3'
down_revision = '6b3f585288d7'
branch_labels = None
depends_on = None


def column_exists(connection, table_name, column_name):
    """Check if a column exists in the specified table."""
    inspector = Inspector.from_engine(connection)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    connection = op.get_bind()

    # Check if the 'lastActivityTimestamp' column exists before adding it
    if not column_exists(connection, "sellers", "lastActivityTimestamp"):
        op.add_column('sellers', sa.Column('lastActivityTimestamp', sa.DateTime(), nullable=True))
        print("Added column 'lastActivityTimestamp' to 'sellers'.")
    else:
        print("Column 'lastActivityTimestamp' already exists in 'sellers'. Skipping addition.")


def downgrade():
    connection = op.get_bind()

    # Check if the 'lastActivityTimestamp' column exists before dropping it
    if column_exists(connection, "sellers", "lastActivityTimestamp"):
        op.drop_column('sellers', 'lastActivityTimestamp')
        print("Dropped column 'lastActivityTimestamp' from 'sellers'.")
    else:
        print("Column 'lastActivityTimestamp' does not exist in 'sellers'. Skipping drop.")
