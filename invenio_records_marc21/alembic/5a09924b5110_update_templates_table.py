# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Update template table."""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from invenio_db import db
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5a09924b5110"
down_revision = "ed55fea7131e"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    """Upgrade database."""
    op.drop_table("marc21_templates")

    op.create_table(
        "marc21_templates",
        sa.Column(
            "created",
            db.UTCDateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated",
            db.UTCDateTime(),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sqlalchemy_utils.types.json.JSONType().with_variant(
                sa.dialects.postgresql.JSON(none_as_null=True),
                "postgresql",
            ),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade database."""
    op.drop_table("marc21_templates")
    op.create_table(
        "marc21_templates",
        sa.Column(
            "created",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column(
            "values",
            sa.JSON()
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marc21_templates")),
        sa.UniqueConstraint("name", name=op.f("uq_marc21_templates_name")),
    )
