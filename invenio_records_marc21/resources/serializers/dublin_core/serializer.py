# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Dublin Core Serializer for Invenio Marc21 Records."""

from flask_resources.serializers import JSONSerializer, MarshmallowSerializer

from .schema import DublinCoreSchema


class Marc21ToDublinCoreJSONSerializer(MarshmallowSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self, **options):
        """Constructor."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=DublinCoreSchema,
            **options
        )
