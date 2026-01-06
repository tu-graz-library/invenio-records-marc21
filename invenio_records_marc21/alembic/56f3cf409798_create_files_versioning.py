# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Update template table."""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "56f3cf409798"
down_revision = "5a09924b5110"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    """Upgrade database."""
    op.create_table(
        "marc21_records_files_version",
        sa.Column(
            "created",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
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
        sa.Column(
            "key",
            sa.Text(),
            nullable=False,
        ),
        sa.Column("record_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "object_version_id",
            sqlalchemy_utils.types.uuid.UUIDType(),
            nullable=True,
        ),
        sa.Column(
            "transaction_id",
            sa.BigInteger(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SMALLINT(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", "transaction_id", name=op.f("pk_marc21_records_files_version")
        ),
    )
    op.create_index(
        "ix_marc21_records_files_version_end_transaction_id",
        "marc21_records_files_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        "ix_marc21_records_files_version_operation_type",
        "marc21_records_files_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        "ix_marc21_records_files_version_transaction_id",
        "marc21_records_files_version",
        ["transaction_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade database."""
    op.drop_table("marc21_records_files_version")
