# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 UI record response serializers."""

from flask_resources import BaseListSchema, JSONSerializer, MarshmallowSerializer

from .schema import Marc21UISchema


class Marc21UIBASESerializer(MarshmallowSerializer):
    """UI Base serializer implementation."""

    def __init__(self):
        """Marc21 UI Base Constructor.

        :param object_key: str key dump ui specific information
        """
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=Marc21UISchema,
            list_schema_cls=BaseListSchema,
        )


class Marc21UIJSONSerializer(Marc21UIBASESerializer):
    """UI JSON serializer implementation."""
