# -*- coding: utf-8 -*-
#
# # Copyright (C) 2024 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Search dumpers for access-control information."""

from flask import current_app
from invenio_rdm_records.records.dumpers import StatisticsDumperExt
from invenio_records.dictutils import dict_lookup

from ..statistics import Marc21Statistics


class Marc21StatisticsDumperExt(StatisticsDumperExt):
    """Search dumper extension for record statistics.

    On dump, it fetches the record's download & view statistics via Invenio-Stats
    queries and dumps them into a field so that they are indexed in the search engine.
    On load, it keeps the dumped values in the data dictionary, in order to enable
    the record schema to dump them if present.
    """

    def dump(self, record, data):
        """Dump the download & view statistics to the data dictionary."""
        if record.is_draft:
            return

        recid = record.pid.pid_value
        parent_recid = record.parent.pid.pid_value

        try:
            parent_data = dict_lookup(data, self.keys, parent=True)
            parent_data[self.key] = Marc21Statistics.get_record_stats(
                recid=recid, parent_recid=parent_recid
            )
        except KeyError as e:
            current_app.logger.warning(e)
