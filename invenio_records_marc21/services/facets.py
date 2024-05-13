# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service facets config."""


from invenio_i18n import gettext as _
from invenio_records_resources.services.records.facets import TermsFacet

is_published = TermsFacet(
    field="is_published",
    label=_("Status"),
    value_labels={"true": _("Published"), "false": _("Not published")},
)


filetype = TermsFacet(
    field="files.types",
    label=_("File type"),
    value_labels=lambda ids: {id: id.upper() for id in ids},
)
