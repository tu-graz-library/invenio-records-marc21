# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
