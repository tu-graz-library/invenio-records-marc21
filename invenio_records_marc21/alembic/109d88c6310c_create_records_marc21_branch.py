# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Create Records Marc21 Branch."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "109d88c6310c"
down_revision = None
branch_labels = ("invenio_records_marc21",)
depends_on = "dbdbc1b19cf2"


def upgrade():
    """Upgrade database."""
    pass


def downgrade():
    """Downgrade database."""
    pass
