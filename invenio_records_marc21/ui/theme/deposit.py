# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 records deposit backend."""


from flask import current_app
from invenio_i18n.ext import current_i18n
from invenio_rdm_records.services.schemas.utils import dump_empty

from invenio_records_marc21.services.schemas import Marc21RecordSchema

from ...proxies import current_records_marc21


def empty_record():
    """Create an empty record."""
    record = dump_empty(Marc21RecordSchema)
    record["metadata"] = "<record><leader>00000nam a2200000zca4500</leader></record>"
    record["access"] = {"record": "public", "files": "public"}
    record["files"] = {"enabled": True}
    record["status"] = "draft"
    return record


def deposit_templates():
    """Retrieve from DB the tamplates for marc21 deposit form."""
    templates = current_records_marc21.templates_service.get_templates()

    if templates:
        return [template.to_dict() for template in templates]
    return []


def deposit_config(**kwargs):
    """Create an deposit configuration."""
    app_config = current_app.config
    jsonschema = current_app.extensions["invenio-jsonschemas"]
    schema = {}
    if jsonschema:
        schema = jsonschema.get_schema(path="marc21/marc21-structure-v1.0.0.json")
    config = dict(
        current_locale=str(current_i18n.locale),
        default_locale=app_config.get("BABEL_DEFAULT_LOCALE", "en"),
        error="",
        schema=schema,
        quota=app_config.get("APP_RDM_DEPOSIT_FORM_QUOTA"),
        createUrl="/api/marc21",
        apiHeaders=app_config.get("INVENIO_MARC21_API_HEADERS"),
        # UploadFilesToolbar  disable file upload
        canHaveMetadataOnlyRecords=True,
        **kwargs
    )
    return config
