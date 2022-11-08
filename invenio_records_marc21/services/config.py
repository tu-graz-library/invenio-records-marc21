# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service config."""


from flask_babelex import gettext as _
from invenio_drafts_resources.services.records.components import DraftFilesComponent
from invenio_drafts_resources.services.records.config import (
    RecordServiceConfig,
    SearchDraftsOptions,
    SearchOptions,
    is_draft,
    is_record,
)
from invenio_rdm_records.records.systemfields.access.field.record import (
    AccessStatusEnum,
)
from invenio_rdm_records.services.components import AccessComponent
from invenio_rdm_records.services.config import has_doi, is_record_and_has_doi
from invenio_records_resources.services import (
    ConditionalLink,
    FileServiceConfig,
    pagination_links,
)
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    SearchOptionsMixin,
)
from invenio_records_resources.services.base.links import Link
from invenio_records_resources.services.files.links import FileLink
from invenio_records_resources.services.records.facets import TermsFacet
from invenio_records_resources.services.records.links import RecordLink

from ..records import Marc21Draft, Marc21Parent, Marc21Record
from .components import MetadataComponent, PIDComponent, PIDsComponent
from .customizations import FromConfigPIDsProviders, FromConfigRequiredPIDs
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21ParentSchema, Marc21RecordSchema

access_right_facet = TermsFacet(
    field="access.record",
    label=_("Access status"),
    value_labels={
        AccessStatusEnum.OPEN.value: _("Public"),
        AccessStatusEnum.EMBARGOED.value: _("Embargoed"),
        AccessStatusEnum.RESTRICTED.value: _("Restricted"),
    },
)

is_published_facet = TermsFacet(
    field="is_published",
    label=_("State"),
    value_labels={"true": _("Published"), "false": _("Unpublished")},
)


class Marc21SearchOptions(SearchOptions, SearchOptionsMixin):
    """Search options for record search."""

    facets = {
        "access_right": access_right_facet,
    }


class Marc21SearchDraftsOptions(SearchDraftsOptions, SearchOptionsMixin):
    """Search options for drafts search."""

    facets = {
        "access_right": access_right_facet,
        "is_published": is_published_facet,
    }


class Marc21RecordServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    """Marc21 record service config."""

    # Record class
    record_cls = Marc21Record
    # Draft class
    draft_cls = Marc21Draft
    # Parent class
    parent_record_cls = Marc21Parent

    # Schemas
    schema = Marc21RecordSchema
    schema_parent = Marc21ParentSchema

    # TODO: ussing from invenio-permissions
    permission_policy_cls = Marc21RecordPermissionPolicy

    links_search = pagination_links("{+api}/marc21{?args*}")

    links_search_drafts = pagination_links("{+api}/marc21/draft{?args*}")

    links_search_versions = pagination_links("{+api}/marc21/{id}/versions{?args*}")

    components = [
        MetadataComponent,
        AccessComponent,
        DraftFilesComponent,
        PIDComponent,
        PIDsComponent,
    ]

    links_item = {
        "self": ConditionalLink(
            cond=is_record,
            if_=RecordLink("{+api}/marc21/{id}"),
            else_=RecordLink("{+api}/marc21/{id}/draft"),
        ),
        "self_html": ConditionalLink(
            cond=is_record,
            if_=RecordLink("{+ui}/marc21/{id}"),
            else_=RecordLink("{+ui}/marc21/uploads/{id}"),
        ),
        "self_doi": Link(
            "{+ui}/marc21/{+pid_doi}",
            when=is_record_and_has_doi,
            vars=lambda record, vars: vars.update(
                {
                    f"pid_{scheme}": pid["identifier"].split("/")[1]
                    for (scheme, pid) in record.pids.items()
                }
            ),
        ),
        "doi": Link(
            "https://doi.org/{+pid_doi}",
            when=has_doi,
            vars=lambda record, vars: vars.update(
                {
                    f"pid_{scheme}": pid["identifier"]
                    for (scheme, pid) in record.pids.items()
                }
            ),
        ),
        "files": ConditionalLink(
            cond=is_record,
            if_=RecordLink("{+api}/marc21/{id}/files"),
            else_=RecordLink("{+api}/marc21/{id}/draft/files"),
        ),
        "latest": RecordLink("{+api}/marc21/{id}/versions/latest"),
        "latest_html": RecordLink("{+ui}/marc21/{id}/latest"),
        "draft": RecordLink("{+api}/marc21/{id}/draft", when=is_record),
        "publish": RecordLink(
            "{+api}/marc21/{id}/draft/actions/publish", when=is_draft
        ),
        "versions": RecordLink("{+api}/marc21/{id}/versions"),
    }

    # PIDs providers - set from config in customizations.
    pids_providers = FromConfigPIDsProviders(
        persistent_identifiers="INVENIO_MARC21_PERSISTENT_IDENTIFIERS",
        persistent_identifier_providers="INVENIO_MARC21_PERSISTENT_IDENTIFIER_PROVIDERS",
    )
    pids_required = FromConfigRequiredPIDs(
        persistent_identifiers="INVENIO_MARC21_PERSISTENT_IDENTIFIERS",
    )


#
# Record files
#
class Marc21RecordFilesServiceConfig(FileServiceConfig, ConfiguratorMixin):
    """Marc21 record files service configuration."""

    record_cls = Marc21Record
    permission_policy_cls = Marc21RecordPermissionPolicy
    permission_action_prefix = ""

    file_links_list = {
        "self": RecordLink("{+api}/marc21/{id}/files"),
    }

    file_links_item = {
        "self": FileLink("{+api}/marc21/{id}/files/{key}"),
        "content": FileLink("{+api}/marc21/{id}/files/{key}/content"),
    }


#
# Draft files
#
class Marc21DraftFilesServiceConfig(FileServiceConfig, ConfiguratorMixin):
    """Marc21 draft files service configuration."""

    record_cls = Marc21Draft
    permission_policy_cls = Marc21RecordPermissionPolicy
    permission_action_prefix = "draft_"

    file_links_list = {
        "self": RecordLink("{+api}/marc21/draft/{id}/files"),
    }

    file_links_item = {
        "self": FileLink("{+api}/marc21/{id}/draft/files/{key}"),
        "content": FileLink("{+api}/marc21/{id}/draft/files/{key}/content"),
        "commit": FileLink("{+api}/marc21/{id}/draft/files/{key}/commit"),
    }
