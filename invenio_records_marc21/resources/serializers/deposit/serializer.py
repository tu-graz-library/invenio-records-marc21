# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 record response serializers."""

from flask_resources import BaseListSchema, JSONSerializer, MarshmallowSerializer

from .schema import Marc21DepositSchema


class Marc21DepositSerializer(MarshmallowSerializer):
    """Marc21 deposit serializer."""

    def __init__(self):
        """Marc21 Base Serializer Constructor.

        :param schema_cls: Default Marc21Schema
        :param options: Json encoding options.
        """
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=Marc21DepositSchema,
            list_schema_cls=BaseListSchema,
        )
