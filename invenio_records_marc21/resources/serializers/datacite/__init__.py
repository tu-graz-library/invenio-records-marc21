# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""DataCite Serializers for Invenio Marc21 Records."""

from flask_resources.serializers import JSONSerializer, MarshmallowSerializer

from .schema import Marc21DataCite43Schema


class Marc21DataCite43JSONSerializer(MarshmallowSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=Marc21DataCite43Schema,
        )

    # TODO: Remove when invenio_rdm_records.services.pids.providers.datacite.DataCitePIDProvider
    # uses the new MarshmallowSerializer class
    def dump_one(self, obj: dict) -> dict:
        """Dump the object with extra information."""
        return self.dump_obj(obj)
