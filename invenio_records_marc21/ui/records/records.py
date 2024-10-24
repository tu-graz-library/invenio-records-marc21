# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Routes for record-related pages provided by Invenio-App-RDM."""

from os.path import splitext

from flask import abort, current_app, render_template, request, url_for
from invenio_base.utils import obj_or_import_string
from invenio_previewer.extensions import default
from invenio_previewer.proxies import current_previewer
from invenio_stats.proxies import current_stats

from ...resources.serializers.ui import Marc21UIJSONSerializer
from .decorators import (
    pass_file_item,
    pass_file_metadata,
    pass_is_preview,
    pass_record_files,
    pass_record_or_draft,
)


class PreviewFile:
    """Preview file implementation for InvenioRDM.

    This class was apparently created because of subtle differences with
    `invenio_previewer.api.PreviewFile`.
    """

    def __init__(self, file_item, record_pid_value, url=None):
        """Create a new PreviewFile."""
        self.file = file_item
        self.data = file_item.data
        self.size = self.data["size"]
        self.filename = self.data["key"]
        self.bucket = self.data["bucket_id"]
        self.uri = url or url_for(
            "invenio_app_rdm_records.record_file_download",
            pid_value=record_pid_value,
            filename=self.filename,
        )

    def is_local(self):
        """Check if file is local."""
        return True

    def has_extensions(self, *exts):
        """Check if file has one of the extensions.

        Each `exts` has the format `.{file type}` e.g. `.txt` .
        """
        file_ext = splitext(self.data["key"])[1].lower()
        return file_ext in exts

    def open(self):
        """Open the file."""
        return self.file._file.file.storage().open()


#
# Views
#
@pass_record_or_draft
@pass_record_files
def record_detail(record=None, files=None, pid_value=None, is_preview=False):
    """Record detail page (aka landing page)."""
    files_dict = None if files is None else files.to_dict()

    # emit a record view stats event
    emitter = current_stats.get_event_emitter("marc21-record-view")
    if record is not None and emitter is not None:
        emitter(current_app, record=record._record, via_api=False)

    ui_record = Marc21UIJSONSerializer().dump_obj(record.to_dict())

    return render_template(
        "invenio_records_marc21/landing_page/record.html",
        record=ui_record,
        pid=pid_value,
        files=files_dict,
        permissions=record.has_permissions_to(
            ["edit", "new_version", "manage", "update_draft", "read_files"]
        ),
        is_preview=is_preview,
        is_draft=record._record.is_draft,
    )


@pass_is_preview
@pass_record_or_draft
def record_export(
    record=None,
    export_format=None,
    pid_value=None,
    permissions=None,
    is_preview=False,
):
    """Export marc21 record page view."""
    exporter = current_app.config.get("MARC21_RECORD_EXPORTERS", {}).get(export_format)
    if exporter is None:
        abort(404)

    serializer = obj_or_import_string(exporter["serializer"])(
        **exporter.get("params", {})
    )
    exported_record = serializer.serialize_object(record.to_dict())
    contentType = exporter.get("content-type", export_format)
    filename = exporter.get("filename", export_format).format(id=pid_value)
    headers = {
        "Content-Type": contentType,
        "Content-Disposition": f"attachment; filename={filename}",
    }
    return (exported_record, 200, headers)


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
    **kwargs,
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

    # emit a file download stats event
    emitter = current_stats.get_event_emitter("marc21-file-download")
    if file_item is not None and emitter is not None:
        obj = file_item._file.object_version
        emitter(current_app, record=file_item._record, obj=obj, via_api=False)

    return file_item.send_file(as_attachment=download)
