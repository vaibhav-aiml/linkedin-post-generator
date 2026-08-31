"""Add document_context column to posts table

Revision ID: 002_add_document_context
Revises: 001_initial_schema
Create Date: 2026-08-31 18:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_add_document_context'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('posts')]
    if 'document_context' not in columns:
        with op.batch_alter_table('posts', schema=None) as batch_op:
            batch_op.add_column(sa.Column('document_context', sa.Text(), nullable=True))


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('posts')]
    if 'document_context' in columns:
        with op.batch_alter_table('posts', schema=None) as batch_op:
            batch_op.drop_column('document_context')

