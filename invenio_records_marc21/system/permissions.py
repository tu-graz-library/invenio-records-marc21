# SPDX-FileCopyrightText: 2025-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Resources configuration."""

from invenio_records_permissions.policies.base import BasePermissionPolicy

from ..services.generators import Marc21RecordManagers


class TemplatePermissionPolicy(BasePermissionPolicy):
    """Template permission policy."""

    can_search = (Marc21RecordManagers(),)
    can_create = (Marc21RecordManagers(),)
    can_read = (Marc21RecordManagers(),)
    can_update = (Marc21RecordManagers(),)
    can_delete = (Marc21RecordManagers(),)
