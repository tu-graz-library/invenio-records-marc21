# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Services exceptions."""


class Marc21RecordsException(Exception):
    """Base exception for Marc21Records errors."""


class EmbargoNotLiftedError(Marc21RecordsException):
    """Embargo could not be lifted ."""

    def __init__(self, record_id: str) -> None:
        """Construct error."""
        super().__init__(f"Embargo could not be lifted for record: {record_id}")
