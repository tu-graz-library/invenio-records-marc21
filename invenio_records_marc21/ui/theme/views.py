# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Routes for general pages provided by Invenio-Records-Marc21."""

from flask import render_template
from flask_login import login_required

from invenio_records_marc21.resources.serializers.ui import Marc21UIXMLSerializer

from .decorators import pass_draft, pass_draft_files
from .deposit import deposit_config, deposit_templates, empty_record


def index():
    """Frontpage."""
    return render_template("invenio_records_marc21/index.html")


def search():
    """Search help guide."""
    return render_template("invenio_records_marc21/search.html")


@login_required
def deposit_create():
    """Create a new deposit page."""
    return render_template(
        "invenio_records_marc21/deposit.html",
        record=empty_record(),
        files=dict(default_preview=None, entries=[], links={}),
        templates=deposit_templates(),
        forms_config=deposit_config(),
    )


@login_required
@pass_draft
@pass_draft_files
def deposit_edit(draft=None, draft_files=None, pid_value=None):
    """Edit an existing deposit."""
    serializer = Marc21UIXMLSerializer()
    record = serializer.dump_obj(draft.to_dict())

    return render_template(
        "invenio_records_marc21/deposit.html",
        forms_config=deposit_config(apiUrl=f"/api/marc21/{pid_value}/draft"),
        record=record,
        files=draft_files.to_dict(),
        permissions=draft.has_permissions_to(["new_version"]),
    )
