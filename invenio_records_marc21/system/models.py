# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 Templates models."""

from invenio_db import db
from invenio_records.models import RecordMetadataBase


class Marc21TemplateMetadata(db.Model, RecordMetadataBase):
    """Templates metadata model."""

    __tablename__ = "marc21_templates"
