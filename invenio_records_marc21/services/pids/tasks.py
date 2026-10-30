# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""RDM PIDs Service tasks."""

from celery import shared_task
from invenio_access.permissions import system_identity

from ...proxies import current_records_marc21


@shared_task(ignore_result=True)
def register_or_update_pid(recid: str, scheme: str) -> None:
    """Update a PID on the remote provider."""
    current_records_marc21.records_service.pids.register_or_update(
        id_=recid,
        identity=system_identity,
        scheme=scheme,
    )
