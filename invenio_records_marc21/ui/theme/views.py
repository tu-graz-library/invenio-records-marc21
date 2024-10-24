# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Routes for general pages provided by Invenio-Records-Marc21."""

from flask import g, render_template
from flask_login import current_user, login_required
from invenio_users_resources.proxies import current_user_resources

from invenio_records_marc21.resources.serializers.deposit import Marc21DepositSerializer

from .decorators import pass_draft, pass_draft_files
from .deposit import deposit_config, deposit_templates, empty_record


def index():
    """Frontpage."""
    return render_template("invenio_records_marc21/index.html")


def search():
    """Search help guide."""
    return render_template("invenio_records_marc21/search/search.html")


@login_required
def uploads_marc21():
    """Display user dashboard page."""
    url = current_user_resources.users_service.links_item_tpl.expand(
        identity=g.identity, obj=current_user
    )["avatar"]
    return render_template(
        "invenio_records_marc21/user_dashboard/uploads.html",
        user_avatar=url,
    )


@login_required
def deposit_create():
    """Create a new deposit page."""
    return render_template(
        "invenio_records_marc21/deposit/index.html",
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
    serializer = Marc21DepositSerializer()
    record = serializer.dump_obj(draft.to_dict())

    return render_template(
        "invenio_records_marc21/deposit/index.html",
        forms_config=deposit_config(apiUrl=f"/api/publications/{pid_value}/draft"),
        record=record,
        files=draft_files.to_dict(),
        permissions=draft.has_permissions_to(["new_version"]),
    )
