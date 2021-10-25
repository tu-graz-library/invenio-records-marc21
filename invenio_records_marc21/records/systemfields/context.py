# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""System field context for the Marc21 PID field.

The context overrides the PID resolver to be aware of the vocabulary type, and
hence the PID type.

The context is used when you initialise a PIField, for instance:

.. code-block:: python

    class Marc21Draft(Draft):
        pid = PIDField(
            'id',
            provider=MarcDraftProvider,
            context_cls=MarcPIDFieldContext
        )

You can then resolve marc21 records using the type:

.. code-block:: python

    Marc21Draft.pid.resolve('<pid_value>')

"""

from invenio_records.systemfields import RelatedModelFieldContext


class MarcPIDFieldContext(RelatedModelFieldContext):
    """PIDField context for Marc21 records.

    This class implements the class-level methods available on a PIDField
    for marc21 records.
    """

    pid_type = "marcid"

    def create(self, record):
        """Proxy to the field's create method."""
        return self.field.create(record)

    def delete(self, record):
        """Proxy to the field's delete method."""
        return self.field.delete(record)

    def resolve(self, pid_value, registered_only=False):
        """Resolve identifier.

        :params pid_value: marc21 record pid.
        """
        # Create resolver
        resolver = self.field._resolver_cls(
            pid_type=self.pid_type,
            object_type=self.field._object_type,
            getter=self.record_cls.get_record,
        )

        # Resolve
        pid, record = resolver.resolve(pid_value)

        # Store pid in cache on record.
        self.field._set_cache(record, pid)

        return record
