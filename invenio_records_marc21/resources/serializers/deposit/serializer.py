# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record response serializers."""

from flask_resources.serializers import JSONSerializer

from ..serializer import Marc21BASESerializer
from .schema import Marc21DepositSchema


class Marc21DepositSerializer(Marc21BASESerializer):
    """Marc21 deposit serializer."""

    def __init__(
        self,
        format_serializer_cls=JSONSerializer,
        object_schema_cls=Marc21DepositSchema,
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
