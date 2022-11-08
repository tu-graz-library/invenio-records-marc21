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

from invenio_records_permissions.generators import AnyUser, Disable, SystemProcess
from invenio_records_permissions.policies.records import RecordPermissionPolicy


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

    # TODO: Change all below when permissions settled
    can_create = [AnyUser()]
    can_update_files = [AnyUser()]
    can_publish = [AnyUser()]
    can_read = [AnyUser()]
    can_update = [AnyUser()]
    can_new_version = [AnyUser()]
    can_edit = [AnyUser()]
    can_lift_embargo = [AnyUser()]
    can_search = [AnyUser(), SystemProcess()]

    # Draft permissions
    can_read_draft = [AnyUser()]
    can_delete_draft = [AnyUser()]
    can_update_draft = [AnyUser()]
    can_search_drafts = [AnyUser()]
    can_draft_read_files = [AnyUser()]
    can_draft_create_files = [AnyUser(), SystemProcess()]
    can_draft_update_files = [AnyUser()]
    can_draft_delete_files = [AnyUser()]
    can_draft_commit_files = [AnyUser()]
    # Files permissions
    can_read_files = [AnyUser()]
    can_create_files = [AnyUser(), SystemProcess()]
    can_update_files = [AnyUser()]
    can_delete_files = [AnyUser()]
    can_commit_files = [Disable()]

    #
    # PIDs
    can_pid_create = [AnyUser()]
    can_pid_register = [AnyUser(), SystemProcess()]
    can_pid_update = [AnyUser()]
    can_pid_discard = [AnyUser()]
    can_pid_delete = [AnyUser()]
