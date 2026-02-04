# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Templates models."""

from invenio_records.api import Record

from .models import Marc21TemplateMetadata


class Marc21Template(Record):
    """Marc21 Templates api."""

    model_cls = Marc21TemplateMetadata
