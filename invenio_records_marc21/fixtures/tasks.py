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


def get_user_identity(user_id: int) -> Identity:
    """Get user identity."""
    identity = Identity(user_id)
    identity.provides.add(any_user)
    identity.provides.add(UserNeed(user_id))
    identity.provides.add(authenticated_user)
    identity.provides.add(RoleNeed("Marc21Manager"))
    return identity


@shared_task
def create_demo_record(
    user_id: int,
    data: dict,
    *,
    publish: bool = True,
    create_file: bool = False,
) -> None:
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
        file_id = "file.txt"
        draft_file_service = service.draft_files
        draft_file_service.init_files(identity, draft.id, data=[{"key": file_id}])
        draft_file_service.set_file_content(
            identity,
            draft.id,
            file_id,
            BytesIO(b"test file content"),
        )
        draft_file_service.commit_file(identity, draft.id, file_id)

    if publish:
        service.publish(id_=draft.id, identity=identity)
