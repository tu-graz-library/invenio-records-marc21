# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc PID providers."""

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2


class MarcRecordProvider(RecordIdProviderV2):
    """Marc records identifier provider.

    This PID provider requires a marc21 record to be passed, and relies
    on the marc21 record having an 'id' key and a type defined.
    """

    pid_type = "marcid"


class MarcDraftProvider(MarcRecordProvider):
    """Marc draft records identifier provider.

    This PID provider requires a marc21 draft record to be passed, and relies
    on the marc21 record having an 'id' key and a type defined.
    """

    default_status_with_obj = PIDStatus.NEW

    predefined_pid_value = ""

    @classmethod
    def create(cls, object_type=None, object_uuid=None, options=None, **kwargs):
        """Intermediate step to create the marcid.

        With this intermediate step it is possible to set pre-calculated marcid's.
        """
        if (
            "record" in kwargs and "$schema" in kwargs["record"]
        ) or cls.predefined_pid_value == "":
            return super(MarcDraftProvider, cls).create(
                object_type=object_type, object_uuid=object_uuid, **kwargs
            )
        else:
            kwargs["pid_value"] = cls.predefined_pid_value
            kwargs.setdefault("status", cls.default_status)

            if object_type and object_uuid:
                kwargs["status"] = cls.default_status_with_obj

            return super(RecordIdProviderV2, cls).create(
                object_type=object_type, object_uuid=object_uuid, **kwargs
            )
