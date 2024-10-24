# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record response deserializers."""

from flask_resources import JSONDeserializer

from .schema import Marc21Schema


class Marc21JSONDeserializer(JSONDeserializer):
    """Marc21 json deserializer."""

    def __init__(self, schema=Marc21Schema):
        """Deserializer initialization."""
        self.schema = schema

    def deserialize(self, data):
        """Deserialize the RO-Crate payload."""
        data = super().deserialize(data)
        return self.schema().load(data)
