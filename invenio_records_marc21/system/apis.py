# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 Templates models."""

from invenio_records.api import Record

from .models import Marc21TemplateMetadata


class Marc21Template(Record):
    """Marc21 Templates api."""

    model_cls = Marc21TemplateMetadata
