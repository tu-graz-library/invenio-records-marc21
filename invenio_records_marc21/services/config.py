# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service config."""

from os.path import splitext

from flask import current_app
from invenio_drafts_resources.services.records.config import (
    RecordServiceConfig,
    SearchDraftsOptions,
    SearchOptions,
    SearchVersionsOptions,
    is_record,
)
from invenio_indexer.api import RecordIndexer
from invenio_rdm_records.services import facets as rdm_facets
from invenio_records_resources.services import FileServiceConfig, pagination_links
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    FromConfig,
    FromConfigSearchOptions,
    SearchOptionsMixin,
)
from invenio_records_resources.services.base.links import EndpointLink
from invenio_records_resources.services.files.links import FileLink
from invenio_records_resources.services.records.links import RecordLink

from ..records import Marc21Draft, Marc21Parent, Marc21Record
from . import facets
from .components import DefaultRecordsComponents
from .customizations import FromConfigPIDsProviders, FromConfigRequiredPIDs
from .links import DefaultServiceLinks
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21ParentSchema, Marc21RecordSchema


##### copy pasted from rdm-records start -----
def is_iiif_compatible(file_, ctx):
    """Determine if a file is IIIF compatible."""
    file_ext = splitext(file_.key)[1].replace(".", "").lower()
    return file_ext in current_app.config["IIIF_FORMATS"]


def is_record_or_draft(drafcord):
    """Return if input is a draft or a record."""
    return "record" if is_record(drafcord, {}) else "draft"


def get_iiif_uuid_of_drafcord_from_file_drafcord(file_drafcord, vars):
    """Return IIIF uuid of draft or record associated with RDMFile{Record,Draft}."""
    # Rely on being called with a context (vars) containing pid_value
    # which was a pre-existing assumption at time of writing
    r_or_d = is_record_or_draft(file_drafcord.record)
    return f"{r_or_d}:{vars['pid_value']}"


def get_iiif_uuid_of_file_drafcord(file_drafcord, vars):
    """Return IIIF uuid of a RDMFileRecord or RDMFileDraft."""
    # Rely on being called with a context (vars) containing pid_value
    # which was a pre-existing assumption at time of writing
    prefix = get_iiif_uuid_of_drafcord_from_file_drafcord(file_drafcord, vars)
    return f"{prefix}:{file_drafcord.key}"


##### copy pasted from rdm-records end -----


class Marc21SearchOptions(SearchOptions, SearchOptionsMixin):
    """Search options for record search."""

    facets = {
        "access_status": rdm_facets.access_status,
        "resource_type": facets.resource_type,
    }


class Marc21SearchDraftsOptions(SearchDraftsOptions, SearchOptionsMixin):
    """Search options for drafts search."""

    facets = {
        "access_status": rdm_facets.access_status,
        "is_published": facets.is_published,
        "resource_type": facets.resource_type,
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

    # The `links_item` attribute in the `Marc21RecordServiceConfig` class is using the `FromConfig` helper
    # to dynamically load the configuration for service links from a specified configuration key
    # (`MARC21_RECORDS_SERVICE_LINKS`). If the configuration key is not found, it will default to using
    # `DefaultServiceLinks`.
    links_item = FromConfig(
        "MARC21_RECORDS_SERVICE_LINKS",
        default=DefaultServiceLinks,
    )

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
        "iiif_base": EndpointLink(
            "marc21iiif.base",
            params=["uuid"],
            when=is_iiif_compatible,
            vars=lambda file_drafcord, vars: vars.update(
                {"uuid": get_iiif_uuid_of_file_drafcord(file_drafcord, vars)}
            ),
        ),
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
