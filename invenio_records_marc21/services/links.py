# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service links."""

from invenio_drafts_resources.services.records.config import is_draft, is_record
from invenio_rdm_records.services.config import record_doi_link
from invenio_records_resources.services import ConditionalLink
from invenio_records_resources.services.records.links import RecordEndpointLink

DefaultServiceLinks = {
    "self": ConditionalLink(
        cond=is_record,
        if_=RecordEndpointLink("marc21_records.read"),
        else_=RecordEndpointLink("marc21_records.read_draft"),
    ),
    "self_html": ConditionalLink(
        cond=is_record,
        if_=RecordEndpointLink("invenio_records_marc21.record_detail"),
        else_=RecordEndpointLink("invenio_records_marc21.deposit_edit"),
    ),
    "self_doi": record_doi_link,
    "doi": record_doi_link,
    "files": ConditionalLink(
        cond=is_record,
        if_=RecordEndpointLink("marc21_files.search"),
        else_=RecordEndpointLink("marc21_draft_files.search"),
    ),
    "draft": RecordEndpointLink("marc21_records.read_draft", when=is_record),
    "publish": RecordEndpointLink("marc21_records.publish", when=is_draft),
}
