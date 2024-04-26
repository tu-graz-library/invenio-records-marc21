# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions for Invenio Marc21 Records."""

from invenio_rdm_records.services.generators import IfFileIsLocal, IfRestricted
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

    ############
    #  Records #
    ############

    # Allow to create a record (create a draft)
    can_create = can_manage
    # Allow to put a record in edit mode (create a draft from record)
    can_edit = can_curate
    # Allow publishing a new record or changes to an existing record.
    can_publish = can_curate
    # Allow lifting the embargo of a record.
    can_lift_embargo = can_curate
    # Allow creating a new version of an existing published record.
    can_new_version = can_manage

    can_search = can_all

    # Allow reading metadata of a record
    can_read = [
        IfRestricted("record", then_=can_view, else_=can_all),
    ]
    # Used for search filtering of deleted records
    # cannot be implemented inside can_read - otherwise permission will
    # kick in before tombstone renders
    can_read_deleted = can_curate
    can_read_deleted_files = can_read_deleted
    can_media_read_deleted_files = can_read_deleted_files

    # Record files permissions
    # Allow enabling/disabling files
    can_manage_files = can_curate

    can_read_files = [
        IfRestricted("files", then_=can_view, else_=can_all),
    ]
    can_get_content_files = [
        IfFileIsLocal(then_=can_read_files, else_=[SystemProcess()])
    ]

    # Allow managing record access
    can_manage_record_access = can_curate

    ############
    #  Draft   #
    ############

    # Allow read a draft
    can_read_draft = can_curate
    # Allow deleting/discarding a draft and all associated files
    can_delete_draft = can_curate
    # Allow updating metadata of a draft
    can_update_draft = can_curate
    # Allow ability to search drafts
    can_search_drafts = can_curate

    # Draft files permissions
    # Allow reading files of a draft
    can_draft_read_files = can_curate
    # Allow uploading, updating and deleting files in drafts
    # Same permissions for files needed as draft
    can_draft_create_files = can_curate
    can_draft_update_files = can_curate
    can_draft_delete_files = can_curate
    can_draft_set_content_files = can_curate
    can_draft_commit_files = can_curate

    can_draft_get_content_files = [
        IfFileIsLocal(then_=can_read_files, else_=[SystemProcess()])
    ]

    #######################
    # Media files - draft #
    #######################
    can_draft_media_create_files = can_curate
    can_draft_media_read_files = can_curate
    can_draft_media_set_content_files = [
        IfFileIsLocal(then_=can_curate, else_=[SystemProcess()])
    ]
    can_draft_media_get_content_files = [
        # preview is same as read_files
        IfFileIsLocal(then_=can_curate, else_=[SystemProcess()])
    ]
    can_draft_media_commit_files = [
        # review is the same as create_files
        IfFileIsLocal(then_=can_curate, else_=[SystemProcess()])
    ]
    can_draft_media_update_files = can_curate
    can_draft_media_delete_files = can_curate

    #
    # Media files - record
    #
    can_media_read_files = [
        IfRestricted("record", then_=can_view, else_=can_all),
    ]
    can_media_get_content_files = [
        # note: even though this is closer to business logic than permissions,
        # it was simpler and less coupling to implement this as permission check
        IfFileIsLocal(then_=can_read, else_=[SystemProcess()])
    ]
    can_media_create_files = [Disable()]
    can_media_set_content_files = [Disable()]
    can_media_commit_files = [Disable()]
    can_media_update_files = [Disable()]
    can_media_delete_files = [Disable()]

    #
    # PIDs
    can_pid_create = can_curate
    can_pid_register = can_curate
    can_pid_update = can_curate
    can_pid_discard = can_curate
    can_pid_delete = can_curate

    # Disabled actions
    # - Files update and delete actions via drafts is not support
    can_create_files = [Disable()]
    can_set_content_files = [Disable()]
    can_update_files = [Disable()]
    can_delete_files = [Disable()]
    can_commit_files = [Disable()]

    # TODO: Add permissions for community when we add the feature!

    # Record and user quota (not needed for now)
    # can_manage_quota

    #
    # Miscellaneous
    can_query_stats = [Disable()]
