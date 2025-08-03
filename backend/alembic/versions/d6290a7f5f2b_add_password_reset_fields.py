"""Add password reset fields

Revision ID: d6290a7f5f2b
Revises: c821532bc4eb
Create Date: 2025-08-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6290a7f5f2b'
down_revision = 'c821532bc4eb'
branch_labels = None
depends_on = None


def upgrade():
    # Add reset_token and reset_token_expires_at columns to users table
    op.add_column('users', sa.Column('reset_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires_at', sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f('ix_users_reset_token'), 'users', ['reset_token'], unique=False)


def downgrade():
    # Remove reset_token and reset_token_expires_at columns from users table
    op.drop_index(op.f('ix_users_reset_token'), table_name='users')
    op.drop_column('users', 'reset_token_expires_at')
    op.drop_column('users', 'reset_token')
