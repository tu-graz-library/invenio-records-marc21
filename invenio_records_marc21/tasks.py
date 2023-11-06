# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Celery tasks."""


from celery import shared_task
from flask_principal import Identity
from invenio_access.permissions import any_user, authenticated_user, system_process

from .proxies import current_records_marc21


def system_identity():
    """System identity."""
    identity = Identity(3)
    identity.provides.add(any_user)
    identity.provides.add(authenticated_user)
    identity.provides.add(system_process)
    return identity


@shared_task(ignore_result=True)
def create_marc21_record(data, access):
    """Create records for demo purposes."""
    service = current_records_marc21.records_service
    draft = service.create(
        data=data,
        identity=system_identity(),
        access=access,
    )
    record = service.publish(id_=draft.id, identity=system_identity())

    return record
