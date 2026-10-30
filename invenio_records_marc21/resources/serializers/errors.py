# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Errors for serializers."""


class SerializerError(Exception):
    """Base class for serializer errors."""


class Marc21XMLConvertError(SerializerError):
    """Error thrown when a marc21 xml could not be converted."""
