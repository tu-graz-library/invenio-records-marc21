# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Record deserializers."""

from .deserializer import Marc21JSONDeserializer, Marc21Schema

__all__ = (
    "Marc21JSONDeserializer",
    "Marc21Schema",
)
