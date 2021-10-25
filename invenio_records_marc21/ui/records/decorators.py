# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2019-2021 CERN.
# Copyright (C) 2019-2021 Northwestern University.
# Copyright (C)      2021 TU Wien.
# Copyright (C)      2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Routes for record-related pages provided by Invenio-Records-Marc21."""
from functools import wraps

from flask import g, request
from invenio_records_resources.services.errors import PermissionDeniedError
from sqlalchemy.orm.exc import NoResultFound

from ...proxies import current_records_marc21


def links_config():
    """Get the record links config."""
    return current_records_marc21.record_resource.config.links_config


def draft_links_config():
    """Get the drafts links config."""
    return current_records_marc21.record_resource.config.draft_links_config


def files_service():
    """Get the record files service."""
    return current_records_marc21.records_service.files


def draft_files_service():
    """Get the record files service."""
    return current_records_marc21.records_service.draft_files


def service():
    """Get the record service."""
    return current_records_marc21.records_service


def pass_record_or_draft(f):
    """Decorate to retrieve the record or draft using the record service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        is_preview = kwargs.get("is_preview")

        def get_record():
            """Retrieve record."""
            return service().read(id_=pid_value, identity=g.identity)

        if is_preview:
            try:
                record = service().read_draft(id_=pid_value, identity=g.identity)
            except NoResultFound:
                record = get_record()
        else:
            record = get_record()
        kwargs["record"] = record
        return f(**kwargs)

    return view


def pass_is_preview(f):
    """Decorate a view to check if it's a preview."""

    @wraps(f)
    def view(**kwargs):
        preview = request.args.get("preview")
        is_preview = False
        if preview == "1":
            is_preview = True
        kwargs["is_preview"] = is_preview
        return f(**kwargs)

    return view


def pass_record_files(f):
    """Decorate a view to pass a record's files using the files service."""

    @wraps(f)
    def view(**kwargs):
        is_preview = kwargs.get("is_preview")

        def list_record_files():
            """List record files."""
            return files_service().list_files(id_=pid_value, identity=g.identity)

        try:
            pid_value = kwargs.get("pid_value")
            if is_preview:
                try:
                    files = draft_files_service().list_files(
                        id_=pid_value, identity=g.identity
                    )
                except NoResultFound:
                    files = list_record_files()
            else:
                files = list_record_files()
            kwargs["files"] = files

        except PermissionDeniedError:
            kwargs["files"] = None

        return f(**kwargs)

    return view


# NOTE:
# copy pasted code from invenio_app_rdm/records_ui/views/decorators.py to use
# the local file_service service
def pass_file_item(f):
    """Decorate a view to pass a file item using the files service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        file_key = kwargs.get("filename")
        is_preview = kwargs.get("is_preview")

        def get_record_file_content():
            """Retrieve record file content."""
            return files_service().get_file_content(
                id_=pid_value, file_key=file_key, identity=g.identity
            )

        if is_preview:
            try:
                item = draft_files_service().get_file_content(
                    id_=pid_value, file_key=file_key, identity=g.identity
                )
            except NoResultFound:
                item = get_record_file_content()
        else:
            item = get_record_file_content()
        kwargs["file_item"] = item
        return f(**kwargs)

    return view


# NOTE:
# copy pasted code from invenio_app_rdm/records_ui/views/decorators.py to use
# the local file_service service
def pass_file_metadata(f):
    """Decorate a view to pass a file's metadata using the files service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        file_key = kwargs.get("filename")
        is_preview = kwargs.get("is_preview")

        def get_record_file_content():
            """Retrieve record file metadata."""
            return files_service().read_file_metadata(
                id_=pid_value, file_key=file_key, identity=g.identity
            )

        if is_preview:
            try:
                files = draft_files_service().read_file_metadata(
                    id_=pid_value, file_key=file_key, identity=g.identity
                )
            except NoResultFound:
                files = get_record_file_content()
        else:
            files = get_record_file_content()
        kwargs["file_metadata"] = files
        return f(**kwargs)

    return view


def user_permissions(actions=[]):
    """Decorate a view to pass user's permissions for the provided actions.

    :param actions: The action list to check permissions against.
    """

    def _wrapper_func(f):
        @wraps(f)
        def view(**kwargs):
            action_args = {}
            if "record" in kwargs:
                action_args["record"] = kwargs["record"]._record
            elif "draft" in kwargs:
                action_args["record"] = kwargs["draft"]._record
            permissions = {}
            for action in actions:
                action_can = (
                    service()
                    .permission_policy(action, **action_args)
                    .allows(g.identity)
                )
                permissions[f"can_{action}"] = action_can
            kwargs["permissions"] = permissions
            return f(**kwargs)

        return view

    return _wrapper_func
