# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Add table for metadata_version."""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from invenio_db import db
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "bcf247730972"
down_revision = "4cb1c2e2bf42"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    """Upgrade database."""
    op.create_table(
        "marc21_records_metadata_version",
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
            sa.JSON()
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()),
                "postgresql",
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("index", sa.Integer(), nullable=True),
        sa.Column("bucket_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column("parent_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column("deletion_status", sa.String(length=1), nullable=True),
        sa.Column(
            "transaction_id",
            sa.BigInteger(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id",
            "transaction_id",
            name=op.f("pk_marc21_records_metadata_version"),
        ),
    )
    op.create_index(
        "ix_marc21_records_metadata_version_end_transaction_id",
        "marc21_records_metadata_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        "ix_marc21_records_metadata_version_operation_type",
        "marc21_records_metadata_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        "ix_marc21_records_metadata_version_transaction_id",
        "marc21_records_metadata_version",
        ["transaction_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade database."""
    op.drop_table("marc21_records_metadata_version")
