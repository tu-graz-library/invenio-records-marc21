# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Templates models."""

from invenio_db import db
from invenio_records.models import RecordMetadataBase


class Marc21TemplateMetadata(db.Model, RecordMetadataBase):
    """Templates metadata model."""

    __tablename__ = "marc21_templates"
