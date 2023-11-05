# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resources configuration."""

import marshmallow as ma
from flask_resources import JSONDeserializer, RequestBodyParser, ResponseHandler
from invenio_drafts_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.files import FileResourceConfig
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema

from .serializers import Marc21JSONSerializer, Marc21XMLSerializer
from .serializers.ui import Marc21UIJSONSerializer, Marc21UIXMLSerializer

record_serializer = {
    "application/json": ResponseHandler(Marc21JSONSerializer()),
    "application/marcxml": ResponseHandler(Marc21XMLSerializer()),
    "application/vnd.inveniomarc21.v1+json": ResponseHandler(Marc21UIJSONSerializer()),
    "application/vnd.inveniomarc21.v1+marcxml": ResponseHandler(
        Marc21UIXMLSerializer()
    ),
}

url_prefix = "/publications"

record_ui_routes = {
    "search": "/search",
    "list": "",
    "item": "/<pid_value>",
    "item-versions": "/<pid_value>/versions",
    "item-latest": "/<pid_value>/versions/latest",
    "item-draft": "/<pid_value>/draft",
    "item-publish": "/<pid_value>/draft/actions/publish",
    "item-files-import": "/<pid_value>/draft/actions/files-import",
    "user-prefix": "/user",
}


class Marc21RecordResourceConfig(RecordResourceConfig):
    """Marc21 Record resource configuration."""

    blueprint_name = "marc21_records"
    url_prefix = url_prefix

    default_accept_mimetype = "application/json"

    response_handlers = record_serializer

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }
    links_config = {}

    routes = record_ui_routes

    # Request parsing
    request_args = SearchRequestArgsSchema
    request_view_args = {"pid_value": ma.fields.Str()}
    request_headers = {"if_match": ma.fields.Int()}
    request_body_parsers = {
        "application/json": RequestBodyParser(JSONDeserializer()),
        "application/marcxml": RequestBodyParser(JSONDeserializer()),
    }

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }


class Marc21RecordFilesResourceConfig(FileResourceConfig):
    """Bibliographic record files resource config."""

    allow_upload = False
    blueprint_name = "marc21_files"
    url_prefix = f"{url_prefix}/<pid_value>"


#
# Draft files
#
class Marc21DraftFilesResourceConfig(FileResourceConfig):
    """Bibliographic record files resource config."""

    blueprint_name = "marc21_draft_files"
    url_prefix = f"{url_prefix}/<pid_value>/draft"


class Marc21ParentRecordLinksResourceConfig(RecordResourceConfig):
    """User records resource configuration."""

    blueprint_name = "marc21_access"

    url_prefix = f"{url_prefix}/<pid_value>/access"

    routes = {
        "search": "",
        "list": "/links",
        "item": "/links/<link_id>",
    }

    links_config = {}

    request_view_args = {"pid_value": ma.fields.Str(), "link_id": ma.fields.Str()}

    response_handlers = {"application/json": ResponseHandler(Marc21JSONSerializer())}
