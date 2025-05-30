"""Readers add

Revision ID: a4aa33543909
Revises: 73d1bbf8fd2f
Create Date: 2025-05-22 06:53:02.804684

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4aa33543909"
down_revision: Union[str, None] = "73d1bbf8fd2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "readers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_readers_email"), "readers", ["email"], unique=True)
    op.create_index(op.f("ix_readers_id"), "readers", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_readers_id"), table_name="readers")
    op.drop_index(op.f("ix_readers_email"), table_name="readers")
    op.drop_table("readers")
    # ### end Alembic commands ###
