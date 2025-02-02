"""Initial migration

Revision ID: f5bd624da99f
Revises:
Create Date: 2024-10-29 15:55:59.544459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = 'f5bd624da99f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(connection, table_name):
    """Check if a table exists in the database."""
    inspector = Inspector.from_engine(connection)
    return table_name in inspector.get_table_names()


def upgrade() -> None:
    connection = op.get_bind()

    # Check if the 'sellers' table exists
    if not table_exists(connection, "sellers"):
        # Create the 'sellers' table
        op.create_table(
            'sellers',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=True),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('is_active', sa.String(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )
        print("Table 'sellers' created successfully.")

        # Create indexes for 'sellers' table
        op.create_index(op.f('ix_sellers_id'), 'sellers', ['id'], unique=False)
        op.create_index(op.f('ix_sellers_name'), 'sellers', ['name'], unique=False)
        print("Indexes for 'sellers' created successfully.")
    else:
        print("Table 'sellers' already exists. Skipping creation.")


def downgrade() -> None:
    connection = op.get_bind()

    # Drop the 'sellers' table only if it exists
    if table_exists(connection, "sellers"):
        op.drop_index(op.f('ix_sellers_name'), table_name='sellers')
        op.drop_index(op.f('ix_sellers_id'), table_name='sellers')
        op.drop_table('sellers')
        print("Table 'sellers' and its indexes dropped successfully.")
    else:
        print("Table 'sellers' does not exist. Skipping drop.")
