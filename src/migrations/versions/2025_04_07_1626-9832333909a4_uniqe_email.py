"""uniqe email

Revision ID: 9832333909a4
Revises: 6f4a83199d19
Create Date: 2025-04-07 16:26:49.435195

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9832333909a4"
down_revision: Union[str, None] = "6f4a83199d19"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")

