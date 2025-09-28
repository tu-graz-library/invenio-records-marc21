# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record response serializers."""

# import json

from flask_resources import BaseListSchema, JSONSerializer, MarshmallowSerializer

from .schema import Marc21Schema


class Marc21BASESerializer(MarshmallowSerializer):
    """Marc21 Base serializer implementation."""

    def __init__(self):
        """Marc21 Base Serializer Constructor.

        :param schema_cls: Default Marc21Schema
        :param options: Json encoding options.
        """
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=Marc21Schema,
            list_schema_cls=BaseListSchema,
        )


class Marc21JSONSerializer(Marc21BASESerializer):
    """Marc21 JSON export serializer implementation."""
