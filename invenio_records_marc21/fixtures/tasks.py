# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 fixture tasks."""

from io import BytesIO

from celery import shared_task
from flask_principal import Identity, RoleNeed, UserNeed
from invenio_access.permissions import (
    any_user,
    authenticated_user,
    system_identity,
    system_user_id,
)

from ..proxies import current_records_marc21


def get_user_identity(user_id):
    """Get user identity."""
    identity = Identity(user_id)
    identity.provides.add(any_user)
    identity.provides.add(UserNeed(user_id))
    identity.provides.add(authenticated_user)
    identity.provides.add(RoleNeed("Marc21Manager"))
    return identity


def _add_file_to_draft(draft_file_service, draft_id, file_id, identity):
    """Add a file to the record."""
    draft_file_service.init_files(identity, draft_id, data=[{"key": file_id}])
    draft_file_service.set_file_content(
        identity, draft_id, file_id, BytesIO(b"test file content")
    )
    result = draft_file_service.commit_file(identity, draft_id, file_id)
    return result


@shared_task
def create_demo_record(user_id, data, publish=True, create_file=False):
    """Create demo record."""
    if user_id == system_user_id:
        identity = system_identity
    else:
        identity = get_user_identity(user_id)

    service = current_records_marc21.records_service
    draft = service.create(
        data=data,
        identity=identity,
    )
    if create_file:
        _add_file_to_draft(service.draft_files, draft.id, "file.txt", identity)
    if publish:
        service.publish(id_=draft.id, identity=identity)
