# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2020-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
