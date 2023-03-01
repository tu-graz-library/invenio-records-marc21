# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions for Invenio Marc21 Records."""

from flask import current_app
from invenio_rdm_records.services.generators import IfRestricted
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Disable,
    SystemProcess,
)
from invenio_records_permissions.policies.records import RecordPermissionPolicy

from .generators import Marc21RecordManagers


class Marc21RecordPermissionPolicy(RecordPermissionPolicy):
    """Access control configuration for records.

    Note that even if the array is empty, the invenio_access Permission class
    always adds the ``superuser-access``, so admins will always be allowed.

    - Create action given to everyone for now.
    - Read access given to everyone if public record and given to owners
      always. (inherited)
    - Update access given to record owners. (inherited)
    - Delete access given to admins only. (inherited)
    """

    #
    # High-level permissions (used by low-level)
    #
    can_all = [AnyUser(), SystemProcess()]
    can_authenticated = [AuthenticatedUser(), SystemProcess()]
    can_manage = [
        SystemProcess(),
        Marc21RecordManagers(),
    ]
    can_view = can_manage

    can_create = can_manage
    can_edit = can_manage
    can_publish = can_manage
    can_lift_embargo = can_manage
    can_new_version = can_manage

    # Draft permissions
    can_read_draft = can_manage
    can_delete_draft = can_manage
    can_update_draft = can_manage
    can_search_drafts = can_manage

    # Draft files permissions
    can_draft_read_files = can_manage
    can_draft_create_files = can_manage
    can_draft_update_files = can_manage
    can_draft_delete_files = can_manage
    can_draft_commit_files = can_manage

    # Files permissions
    can_read_files = [
        IfRestricted("files", then_=can_view, else_=can_all),
    ]

    #
    # PIDs
    can_pid_create = can_manage
    can_pid_register = can_manage
    can_pid_update = can_manage
    can_pid_discard = can_manage
    can_pid_delete = can_manage

    # Disabled actions
    can_create_files = [Disable()]
    can_update_files = [Disable()]
    can_delete_files = [Disable()]
    can_commit_files = [Disable()]
