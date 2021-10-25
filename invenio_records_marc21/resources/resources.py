# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Resource."""


from flask_resources import route
from invenio_drafts_resources.resources import RecordResource

from . import config


#
# Records
#
class Marc21RecordResource(RecordResource):
    """Bibliographic record resource."""

    config_name = "MARC21_RECORDS_RECORD_CONFIG"
    default_config = config.Marc21RecordResourceConfig

    def p(self, route):
        """Prefix a route with the URL prefix."""
        return f"{self.config.url_prefix}{route}"

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        url_rules = super(RecordResource, self).create_url_rules()
        return url_rules


class Marc21ParentRecordLinksResource(RecordResource):
    """Secret links resource."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        routes = self.config.routes
        return [
            route("GET", p(routes["list"]), self.search),
            route("POST", p(routes["list"]), self.create),
            route("GET", p(routes["item"]), self.read),
            route("PUT", p(routes["item"]), self.update),
            route("DELETE", p(routes["item"]), self.delete),
        ]
