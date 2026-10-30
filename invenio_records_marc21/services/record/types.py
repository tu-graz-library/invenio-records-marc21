# SPDX-FileCopyrightText: 2022-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 types."""

from dataclasses import dataclass


@dataclass
class Marc21Category:
    """Base type for category."""

    value: str
    category: str

    def __init__(self, value):
        """Constructor of the Marc21Category class."""
        self.value = value

    def __repr__(self):
        """Representation magic method."""
        return self.value

    def __str__(self):
        """String representation magic method."""
        return self.value


class ACNumber(Marc21Category):
    """AC Number category."""

    category: str = "009"


class DOI(Marc21Category):
    """DOI Category."""

    category: str = "552"


class DuplicateRecordError(Exception):
    """Duplicate Record Exception."""

    def __init__(self, value, category, id_):
        """Constructor for class DuplicateRecordException."""
        msg = f"DuplicateRecordError value: {value} with category: {category} already exists id={id_} in the database"
        super().__init__(msg)
