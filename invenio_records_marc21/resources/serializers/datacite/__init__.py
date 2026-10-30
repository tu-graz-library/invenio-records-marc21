# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
