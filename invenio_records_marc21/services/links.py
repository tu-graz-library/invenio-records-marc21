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
from invenio_rdm_records.services.config import has_doi, is_record_and_has_doi
from invenio_records_resources.services import ConditionalLink
from invenio_records_resources.services.base.links import Link
from invenio_records_resources.services.records.links import RecordLink

DefaultServiceLinks = {
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
        vars=lambda record, var_s: var_s.update(
            {
                f"pid_{scheme}": pid["identifier"].split("/")[1]
                for (scheme, pid) in record.pids.items()
                if scheme == "doi"
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
                if scheme == "doi"
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
    "draft": RecordLink("{+ui}/publications/{id}", when=is_record),
    "publish": RecordLink(
        "{+api}/publications/{id}/draft/actions/publish", when=is_draft
    ),
    "versions": RecordLink("{+api}/publications/{id}/versions"),
}
