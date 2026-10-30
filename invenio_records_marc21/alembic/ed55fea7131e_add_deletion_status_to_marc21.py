# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 templates add updated."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ed55fea7131e"
down_revision = "b9f2911d44c7"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # step 1: create the columns, but make them nullable for now
    op.add_column(
        "marc21_records_metadata",
        sa.Column("deletion_status", sa.String(length=1), nullable=True),
    )

    # step 2: set default values for existing rows
    default_value = "P"
    metadata_table = sa.sql.table(
        "marc21_records_metadata", sa.sql.column("deletion_status")
    )
    op.execute(metadata_table.update().values(deletion_status=default_value))

    # step 3: make the original table not nullable
    op.alter_column("marc21_records_metadata", "deletion_status", nullable=False)


def downgrade():
    """Downgrade database."""
    op.drop_column("marc21_records_metadata", "deletion_status")
