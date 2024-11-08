"""Added email and hashed_password

Revision ID: 741300a31496
Revises: f5bd624da99f
Create Date: 2024-10-30 09:43:35.067438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '741300a31496'
down_revision = 'f5bd624da99f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vendors', sa.Column('email', sa.String(), nullable=False))
    op.add_column('vendors', sa.Column('hashed_password', sa.String(), nullable=False))
    op.create_index(op.f('ix_vendors_email'), 'vendors', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vendors_email'), table_name='vendors')
    op.drop_column('vendors', 'hashed_password')
    op.drop_column('vendors', 'email')
    # ### end Alembic commands ###