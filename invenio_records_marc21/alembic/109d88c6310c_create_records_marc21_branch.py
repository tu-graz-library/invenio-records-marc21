# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
