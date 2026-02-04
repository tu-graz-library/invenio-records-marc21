# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service links."""

from flask import current_app
from invenio_drafts_resources.services.records.config import is_draft, is_record
from invenio_records_resources.services import ConditionalLink, ExternalLink
from invenio_records_resources.services.records.links import RecordEndpointLink


def has_doi(record, ctx):
    """Determine if a record has a DOI."""
    pids = record.pids or {}


def is_datacite_test(record, ctx):
    """Return if the datacite test mode is being used."""
    return current_app.config["DATACITE_TEST_MODE"]


class RecordPIDLink(ExternalLink):
    """Record external PID link."""

    def vars(self, record, vars):
        """Add record PID to vars."""
        vars.update(
            {
                f"pid_{scheme}": pid["identifier"]
                for (scheme, pid) in record.pids.items()
            }
        )


record_doi_link = ConditionalLink(
    cond=is_datacite_test,
    if_=RecordPIDLink("https://handle.test.datacite.org/{+pid_doi}", when=has_doi),
    else_=RecordPIDLink("https://doi.org/{+pid_doi}", when=has_doi),
)

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
        if_=RecordEndpointLink("marc21_record_files.search"),
        else_=RecordEndpointLink("marc21_draft_files.search"),
    ),
    "draft": RecordEndpointLink("marc21_records.read_draft", when=is_record),
    "publish": RecordEndpointLink("marc21_records.publish", when=is_draft),
}
