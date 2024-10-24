# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record response serializers."""

import json

from flask_resources.serializers import JSONSerializer, MarshmallowSerializer

from .schema import Marc21Schema


class Marc21BASESerializer(MarshmallowSerializer):
    """Marc21 Base serializer implementation."""

    def __init__(
        self,
        format_serializer_cls=JSONSerializer,
        object_schema_cls=Marc21Schema,
        **options,
    ):
        """Marc21 Base Serializer Constructor.

        :param schema_cls: Default Marc21Schema
        :param options: Json encoding options.
        """
        super().__init__(
            format_serializer_cls=format_serializer_cls,
            object_schema_cls=object_schema_cls,
            **options,
        )

    def dump_obj(self, obj):
        """Dump the object into a JSON string."""
        return self.object_schema.dump(obj)

    def dump_list(self, obj_list):
        """Serialize a list of records.

        :param obj_list: List of records instance.
        """
        records = obj_list["hits"]["hits"]
        obj_list["hits"]["hits"] = [self.dump_obj(obj) for obj in records]
        return obj_list


class Marc21JSONSerializer(Marc21BASESerializer):
    """Marc21 JSON export serializer implementation."""

    def serialize_object_list(self, obj_list):
        """Serialize a list of records.

        :param records: List of records instance.
        """
        obj_list = self.dump_list(obj_list)
        return json.dumps(obj_list, cls=self.format_serializer.encoder)
