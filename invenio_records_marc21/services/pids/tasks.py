# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
