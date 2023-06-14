# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""PIDs provider module."""

from invenio_i18n import lazy_gettext as _
from invenio_rdm_records.services.pids.providers import (
    DataCitePIDProvider as BaseDataCitePIDProvider,
)


class Marc21DataCitePIDProvider(BaseDataCitePIDProvider):
    """Marc21 DataCite pid provider."""

    def validate(self, record, identifier=None, provider=None, **kwargs):
        """Validate the attributes of the identifier.

        :returns: A tuple (success, errors). `success` is a bool that specifies
                  if the validation was successful. `errors` is a list of
                  error dicts of the form:
                  `{"field": <field>, "messages: ["<msgA1>", ...]}`.
        """
        # skip direct parent-class's validate, but do parent's parent
        success, errors = super(BaseDataCitePIDProvider, self).validate(
            record, identifier, provider, **kwargs
        )

        # check format
        if identifier is not None:
            try:
                self.client.api.check_doi(identifier)
            except ValueError as e:
                # modifies the error in errors in-place
                self._insert_pid_type_error_msg(errors, str(e))

        return success and not errors, errors
