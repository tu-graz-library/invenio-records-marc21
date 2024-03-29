# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 templates add updated."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b9f2911d44c7"
down_revision = "0058aec64e36"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "marc21_templates",
        sa.Column(
            "updated",
            sa.DateTime(),
            nullable=True,
        ),
    )
    op.execute("UPDATE marc21_templates SET updated = NOW()")
    op.alter_column("marc21_templates", "updated", nullable=False)
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("marc21_templates", "updated")
    # ### end Alembic commands ###
