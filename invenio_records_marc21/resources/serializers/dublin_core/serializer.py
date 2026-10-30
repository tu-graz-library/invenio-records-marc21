# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Dublin Core Serializer for Invenio Marc21 Records."""

from dcxml import simpledc
from flask_resources import BaseListSchema
from flask_resources.serializers import (
    JSONSerializer,
    MarshmallowSerializer,
    SimpleSerializer,
)

from .schema import DublinCoreSchema


class Marc21ToDublinCoreJSONSerializer(MarshmallowSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self, **options):
        """Constructor."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=DublinCoreSchema,
            **options,
        )


class Marc21ToDublinCoreXMLSerializer(MarshmallowSerializer):
    """Marshmallow based Dublin Core serializer for records.

    Note: This serializer is not suitable for serializing large number of
    records.
    """

    def __init__(self, **kwargs: dict) -> None:
        """Construct."""
        super().__init__(
            format_serializer_cls=SimpleSerializer,
            object_schema_cls=DublinCoreSchema,
            list_schema_cls=BaseListSchema,
            encoder=simpledc.tostring,
            **kwargs,
        )
