# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
