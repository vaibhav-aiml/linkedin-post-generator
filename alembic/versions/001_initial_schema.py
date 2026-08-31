"""Initial schema baseline (users and posts tables)

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-08-31 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # Create users table if not exists
    if 'users' not in existing_tables:
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('hashed_password', sa.String(length=255), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)
            batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)

    # Create posts table if not exists
    if 'posts' not in existing_tables:
        op.create_table(
            'posts',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.Column('topic', sa.String(length=255), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('type', sa.String(length=50), nullable=False),
            sa.Column('date', sa.String(length=50), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('content_hash', sa.String(length=64), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        with op.batch_alter_table('posts', schema=None) as batch_op:
            batch_op.create_index(batch_op.f('ix_posts_id'), ['id'], unique=False)
            batch_op.create_index(batch_op.f('ix_posts_user_id'), ['user_id'], unique=False)
            batch_op.create_index(batch_op.f('ix_posts_topic'), ['topic'], unique=False)
            batch_op.create_index(batch_op.f('ix_posts_type'), ['type'], unique=False)
            batch_op.create_index(batch_op.f('ix_posts_content_hash'), ['content_hash'], unique=True)


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'posts' in existing_tables:
        with op.batch_alter_table('posts', schema=None) as batch_op:
            try:
                batch_op.drop_index(batch_op.f('ix_posts_content_hash'))
                batch_op.drop_index(batch_op.f('ix_posts_type'))
                batch_op.drop_index(batch_op.f('ix_posts_topic'))
                batch_op.drop_index(batch_op.f('ix_posts_user_id'))
                batch_op.drop_index(batch_op.f('ix_posts_id'))
            except Exception:
                pass
        op.drop_table('posts')

    if 'users' in existing_tables:
        with op.batch_alter_table('users', schema=None) as batch_op:
            try:
                batch_op.drop_index(batch_op.f('ix_users_email'))
                batch_op.drop_index(batch_op.f('ix_users_id'))
            except Exception:
                pass
        op.drop_table('users')

