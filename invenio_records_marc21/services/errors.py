# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Services exceptions."""


class Marc21RecordsException(Exception):
    """Base exception for Marc21Records errors."""


class EmbargoNotLiftedError(Marc21RecordsException):
    """Embargo could not be lifted ."""

    def __init__(self, record_id: str) -> None:
        """Construct error."""
        super().__init__(f"Embargo could not be lifted for record: {record_id}")
