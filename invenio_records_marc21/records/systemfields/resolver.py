# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc PID resolver."""

from collections.abc import Callable

from invenio_pidstore.resolver import Resolver


class MarcResolver(Resolver):
    """Marc21 Persistent identifier resolver.

    Helper class for retrieving an internal object for a given persistent
    identifier.
    """

    def __init__(
        self,
        pid_type: str = "marcid",
        object_type: str = "rec",
        getter: Callable | None = None,
        *,
        registered_only: bool = False,
    ) -> None:
        """Initialize resolver.

        :param pid_type: Persistent identifier type.
        :param object_type: Object type.
        :param getter: Callable that will take an object id for the given
            object type and retrieve the internal object.
        """
        self.pid_type = pid_type
        self.object_type = object_type
        self.object_getter = getter
        self.registered_only = registered_only
