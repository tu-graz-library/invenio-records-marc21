# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record components."""

from invenio_drafts_resources.services.records.components import DraftFilesComponent
from invenio_rdm_records.services.components import AccessComponent

from .metadata import MetadataComponent
from .pid import PIDComponent
from .pids import ParentPIDsComponent, PIDsComponent

DefaultRecordsComponents = [
    MetadataComponent,
    AccessComponent,
    DraftFilesComponent,
    PIDComponent,
    PIDsComponent,
    ParentPIDsComponent,
]

__all__ = ("DefaultRecordsComponents",)
