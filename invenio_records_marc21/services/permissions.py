# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions for Invenio Marc21 Records."""

from invenio_rdm_records.services.generators import IfRestricted
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Disable,
    SystemProcess,
)
from invenio_records_permissions.policies.records import RecordPermissionPolicy

from .generators import Marc21RecordCurators, Marc21RecordManagers


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
    can_manage = [Marc21RecordManagers(), SystemProcess()]
    can_curate = can_manage + [Marc21RecordCurators()]
    can_view = can_curate

    can_create = can_manage
    can_edit = can_curate
    can_publish = can_curate
    can_lift_embargo = can_curate
    can_new_version = can_manage

    #  Records
    can_search = can_all
    # Allow reading metadata of a record
    can_read = [
        IfRestricted("record", then_=can_view, else_=can_all),
    ]
    # Files permissions
    can_read_files = [
        IfRestricted("files", then_=can_view, else_=can_all),
    ]

    # Draft
    can_read_draft = can_curate
    can_delete_draft = can_curate
    can_update_draft = can_curate
    can_search_drafts = can_curate

    # Draft files permissions
    can_draft_read_files = can_curate
    can_draft_create_files = can_curate
    can_draft_update_files = can_curate
    can_draft_delete_files = can_curate
    can_draft_set_content_files = can_curate
    can_draft_commit_files = can_curate

    #
    # PIDs
    can_pid_create = can_curate
    can_pid_register = can_curate
    can_pid_update = can_curate
    can_pid_discard = can_curate
    can_pid_delete = can_curate

    # Disabled actions
    can_create_files = [Disable()]
    can_update_files = [Disable()]
    can_delete_files = [Disable()]
    can_commit_files = [Disable()]
