# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Alter utc unaware columns to utc aware columns."""

from invenio_db.utils import (
    update_table_columns_column_type_to_datetime,
    update_table_columns_column_type_to_utc_datetime,
)

# revision identifiers, used by Alembic.
revision = "4cb1c2e2bf42"
down_revision = "56f3cf409798"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    """Upgrade database."""
    for table_name in [
        "marc21_parents_metadata",
        "marc21_records_metadata",
        "marc21_drafts_metadata",
        "marc21_drafts_files",
        "marc21_records_files",
        "marc21_records_files_version",
    ]:
        update_table_columns_column_type_to_utc_datetime(table_name, "created")
        update_table_columns_column_type_to_utc_datetime(table_name, "updated")
    update_table_columns_column_type_to_utc_datetime(
        "marc21_drafts_metadata", "expires_at"
    )


def downgrade() -> None:
    """Downgrade database."""
    for table_name in [
        "marc21_parents_metadata",
        "marc21_records_metadata",
        "marc21_drafts_metadata",
        "marc21_drafts_files",
        "marc21_records_files",
        "marc21_records_files_version",
    ]:
        update_table_columns_column_type_to_datetime(table_name, "created")
        update_table_columns_column_type_to_datetime(table_name, "updated")
    update_table_columns_column_type_to_datetime("marc21_drafts_metadata", "expires_at")
