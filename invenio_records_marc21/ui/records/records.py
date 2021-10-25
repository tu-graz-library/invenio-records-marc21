# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Routes for record-related pages provided by Invenio-App-RDM."""

from flask import abort, current_app, render_template, request, url_for
from invenio_app_rdm.records_ui.views.decorators import pass_is_preview
from invenio_app_rdm.records_ui.views.records import PreviewFile
from invenio_base.utils import obj_or_import_string
from invenio_previewer.extensions import default
from invenio_previewer.proxies import current_previewer

from ...resources.serializers.ui import Marc21UIJSONSerializer
from .decorators import (
    pass_file_item,
    pass_file_metadata,
    pass_record_files,
    pass_record_or_draft,
)


#
# Views
#
@pass_record_or_draft
@pass_record_files
def record_detail(record=None, files=None, pid_value=None, is_preview=False):
    """Record detail page (aka landing page)."""
    files_dict = None if files is None else files.to_dict()
    return render_template(
        "invenio_records_marc21/record.html",
        record=Marc21UIJSONSerializer().dump_one(record.to_dict()),
        pid=pid_value,
        files=files_dict,
        permissions=record.has_permissions_to(
            ["edit", "new_version", "manage", "update_draft", "read_files"]
        ),
        is_preview=is_preview,
        is_draft=record._record.is_draft,
    )


@pass_record_or_draft
def record_export(record=None, export_format=None, pid_value=None, permissions=None):
    """Export marc21 record page view."""
    exporter = current_app.config.get("INVENIO_MARC21_RECORD_EXPORTERS", {}).get(
        export_format
    )
    if exporter is None:
        abort(404)

    options = current_app.config.get(
        "INVENIO_MARC21_RECORD_EXPORTER_OPTIONS",
        {
            "indent": 2,
            "sort_keys": True,
        },
    )

    serializer = obj_or_import_string(exporter["serializer"])(options=options)
    exported_record = serializer.serialize_object(record.to_dict())

    return render_template(
        "invenio_records_marc21/records/export.html",
        pid_value=pid_value,
        export_format=exporter.get("name", export_format),
        exported_record=exported_record,
        record=Marc21UIJSONSerializer().dump_one(record.to_dict()),
        permissions=permissions,
    )


# NOTE:
# copy pasted code from invenio_app_rdm/records_ui/views/records.py with
# minor change invenio_app_rdm_records -> invenio_records_marc21
@pass_is_preview
@pass_record_or_draft
@pass_file_metadata
def record_file_preview(
    record=None,
    pid_value=None,
    pid_type="recid",
    file_metadata=None,
    is_preview=False,
    **kwargs
):
    """Render a preview of the specified file."""

    file_previewer = file_metadata.data.get("previewer")

    url = url_for(
        "invenio_records_marc21.record_file_download",
        pid_value=pid_value,
        filename=file_metadata.data["key"],
        preview=1 if is_preview else 0,
    )
    # Find a suitable previewer
    fileobj = PreviewFile(file_metadata, pid_value, url)
    for plugin in current_previewer.iter_previewers(
        previewers=[file_previewer] if file_previewer else None
    ):
        if plugin.can_preview(fileobj):
            return plugin.preview(fileobj)

    return default.preview(fileobj)


# NOTE:
# copy pasted code from invenio_app_rdm/records_ui/views/records.py with
# minor change invenio_app_rdm_records -> invenio_records_marc21
@pass_is_preview
@pass_file_item
def record_file_download(file_item=None, pid_value=None, is_preview=False, **kwargs):
    """Download a file from a record."""
    download = bool(request.args.get("download"))
    return file_item.send_file(as_attachment=download)
