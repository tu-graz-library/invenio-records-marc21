# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service config."""

from invenio_drafts_resources.services.records.components import DraftFilesComponent
from invenio_drafts_resources.services.records.config import (
    RecordServiceConfig,
    SearchDraftsOptions,
    SearchOptions,
    SearchVersionsOptions,
    is_draft,
    is_record,
)
from invenio_i18n import gettext as _
from invenio_indexer.api import RecordIndexer
from invenio_rdm_records.services import facets as rdm_facets
from invenio_rdm_records.services.components import AccessComponent
from invenio_rdm_records.services.config import has_doi, is_record_and_has_doi
from invenio_records_resources.services import (
    ConditionalLink,
    FileServiceConfig,
    pagination_links,
)
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    FromConfig,
    FromConfigSearchOptions,
    SearchOptionsMixin,
)
from invenio_records_resources.services.base.links import Link
from invenio_records_resources.services.files.links import FileLink
from invenio_records_resources.services.records.links import RecordLink

from ..records import Marc21Draft, Marc21Parent, Marc21Record
from . import facets
from .components import DefaultRecordsComponents
from .customizations import FromConfigPIDsProviders, FromConfigRequiredPIDs
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21ParentSchema, Marc21RecordSchema


class Marc21SearchOptions(SearchOptions, SearchOptionsMixin):
    """Search options for record search."""

    facets = {
        "access_status": rdm_facets.access_status,
    }


class Marc21SearchDraftsOptions(SearchDraftsOptions, SearchOptionsMixin):
    """Search options for drafts search."""

    facets = {
        "access_status": rdm_facets.access_status,
        "is_published": facets.is_published,
    }


class Marc21SearchVersionsOptions(SearchVersionsOptions, SearchOptionsMixin):
    """Search options for record versioning search."""


class Marc21RecordServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    """Marc21 record service config."""

    # Record class
    record_cls = Marc21Record
    # Draft class
    draft_cls = Marc21Draft
    # Parent class
    parent_record_cls = Marc21Parent

    indexer_cls = RecordIndexer
    indexer_queue_name = "marc21-records"
    draft_indexer_cls = RecordIndexer
    draft_indexer_queue_name = "marc21-records-drafts"

    # Schemas
    schema = Marc21RecordSchema
    schema_parent = Marc21ParentSchema

    schema_secret_link = None
    review = None

    # Permission policy
    default_files_enabled = FromConfig("RDM_DEFAULT_FILES_ENABLED", default=True)

    permission_policy_cls = FromConfig(
        "MARC21_PERMISSION_POLICY",
        default=Marc21RecordPermissionPolicy,
        import_string=True,
    )
    # Search
    search = FromConfigSearchOptions(
        "MARC21_SEARCH",
        "MARC21_SORT_OPTIONS",
        "MARC21_FACETS",
        search_option_cls=Marc21SearchOptions,
    )
    search_drafts = FromConfigSearchOptions(
        "MARC21_SEARCH_DRAFTS",
        "MARC21_SORT_OPTIONS",
        "MARC21_FACETS",
        search_option_cls=Marc21SearchDraftsOptions,
    )
    search_versions = FromConfigSearchOptions(
        "MARC21_SEARCH_VERSIONING",
        "MARC21_SORT_OPTIONS",
        "MARC21_FACETS",
        search_option_cls=Marc21SearchVersionsOptions,
    )

    # Permission policy
    default_files_enabled = FromConfig("MARC21_DEFAULT_FILES_ENABLED", default=True)

    permission_policy_cls = FromConfig(
        "MARC21_PERMISSION_POLICY",
        default=Marc21RecordPermissionPolicy,
        import_string=True,
    )
    links_search = pagination_links("{+api}/publications{?args*}")

    links_search_drafts = pagination_links("{+api}/user/publications{?args*}")

    links_search_versions = pagination_links(
        "{+api}/publications/{id}/versions{?args*}"
    )

    components = FromConfig(
        "MARC21_RECORDS_SERVICE_COMPONENTS",
        default=DefaultRecordsComponents,
    )

    links_item = {
        "self": ConditionalLink(
            cond=is_record,
            if_=RecordLink("{+api}/publications/{id}"),
            else_=RecordLink("{+api}/publications/{id}/draft"),
        ),
        "self_html": ConditionalLink(
            cond=is_record,
            if_=RecordLink("{+ui}/publications/{id}"),
            else_=RecordLink("{+ui}/publications/uploads/{id}"),
        ),
        "self_doi": Link(
            "{+ui}/publications/{+pid_doi}",
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
            if_=RecordLink("{+api}/publications/{id}/files"),
            else_=RecordLink("{+api}/publications/{id}/draft/files"),
        ),
        "latest": RecordLink("{+api}/publications/{id}/versions/latest"),
        "latest_html": RecordLink("{+ui}/publications/{id}/latest"),
        "draft": RecordLink("{+api}/publications/{id}/draft", when=is_record),
        "publish": RecordLink(
            "{+api}/publications/{id}/draft/actions/publish", when=is_draft
        ),
        "versions": RecordLink("{+api}/publications/{id}/versions"),
    }

    # PIDs providers - set from config in customizations.
    pids_providers = FromConfigPIDsProviders(
        persistent_identifiers="MARC21_PERSISTENT_IDENTIFIERS",
        persistent_identifier_providers="MARC21_PERSISTENT_IDENTIFIER_PROVIDERS",
    )
    pids_required = FromConfigRequiredPIDs(
        persistent_identifiers="MARC21_PERSISTENT_IDENTIFIERS",
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
        "self": RecordLink("{+api}/publications/{id}/files"),
    }

    file_links_item = {
        "self": FileLink("{+api}/publications/{id}/files/{key}"),
        "content": FileLink("{+api}/publications/{id}/files/{key}/content"),
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
        "self": RecordLink("{+api}/publications/{id}/draft/files"),
    }

    file_links_item = {
        "self": FileLink("{+api}/publications/{id}/draft/files/{key}"),
        "content": FileLink("{+api}/publications/{id}/draft/files/{key}/content"),
        "commit": FileLink("{+api}/publications/{id}/draft/files/{key}/commit"),
    }
