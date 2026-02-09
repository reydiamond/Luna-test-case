"""test seed

Revision ID: a788b728a3dd
Revises: 92740527cc73
Create Date: 2026-02-08 17:53:50.938513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a788b728a3dd'
down_revision: Union[str, Sequence[str], None] = '92740527cc73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
