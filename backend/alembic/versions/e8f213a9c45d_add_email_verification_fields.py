"""Add email verification fields

Revision ID: e8f213a9c45d
Revises: d6290a7f5f2b
Create Date: 2025-08-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8f213a9c45d'
down_revision = 'd6290a7f5f2b'
branch_labels = None
depends_on = None


def upgrade():
    # Add email verification columns to users table
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), server_default='False', nullable=False))
    op.add_column('users', sa.Column('verification_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('verification_token_expires_at', sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f('ix_users_verification_token'), 'users', ['verification_token'], unique=False)


def downgrade():
    # Remove email verification columns from users table
    op.drop_index(op.f('ix_users_verification_token'), table_name='users')
    op.drop_column('users', 'verification_token_expires_at')
    op.drop_column('users', 'verification_token')
    op.drop_column('users', 'email_verified')
