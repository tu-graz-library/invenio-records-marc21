# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""OAI-PMH serializers for Marc21-records."""

from dcxml import simpledc
from flask import g
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier
from invenio_records_resources.services.errors import RecordPermissionDeniedError
from lxml import etree

from .proxies import current_records_marc21
from .records.api import Marc21Record
from .resources.serializers import (
    Marc21OAIXMLSerializer,
    Marc21ToDublinCoreXMLSerializer,
)
from .services.record import Marc21Metadata


def marc21_etree(
    pid: str,  # noqa: ARG001
    record: dict,
) -> dict:
    """Get Marc21 XML for OAI-PMH."""
    return etree.fromstring(
        Marc21OAIXMLSerializer()
        .serialize_object(record["_source"])
        .encode(encoding="utf-8")
    )


def marc21_dc_etree(
    pid: str,  # noqa: ARG001
    record: dict,
) -> dict:
    """Get DublinCore XML etree for OAI-PMH."""
    m21_rec = Marc21Record(record["_source"])
    m21_meta = Marc21Metadata(json=m21_rec["metadata"])
    m21_dc_meta = Marc21ToDublinCoreXMLSerializer().dump_obj(m21_meta)

    return simpledc.dump_etree(m21_dc_meta)


def getrecord_fetcher(record_id: str) -> dict:
    """Fetch record data as dict with identity check for serialization."""
    marc21id = PersistentIdentifier.get_by_object(
        pid_type="marcid",
        object_uuid=record_id,
        object_type="rec",
    )

    try:
        result = current_records_marc21.records_service.read(
            g.identity, marc21id.pid_value
        )
    except RecordPermissionDeniedError as error:
        # if it is a restricted record.
        msg = "marcid"
        raise PIDDoesNotExistError(msg, None) from error

    return result.to_dict()
