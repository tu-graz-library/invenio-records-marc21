#
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test access system field."""


from datetime import timedelta

import arrow
from invenio_rdm_records.records.systemfields.access.field.record import Embargo

#
# Embargo
#


def test_embargo_creation():
    future_date = arrow.utcnow().datetime + timedelta(days=+30)
    embargo = Embargo(
        until=future_date,
        reason="Because I can!",
    )
    assert embargo.active

    past_date = arrow.utcnow().datetime + timedelta(days=-30)
    embargo = Embargo(
        until=past_date,
        reason="espionage",
    )
    assert not embargo.active


def test_embargo_from_dict():
    date_feature = arrow.utcnow().datetime + timedelta(days=+30)
    embargo_dict = {
        "until": date_feature,
        "active": True,
        "reason": "espionage",
    }
    embargo = Embargo.from_dict(embargo_dict)
    assert embargo.active
    assert embargo.until == date_feature
    assert embargo.reason == "espionage"
    embargo_dict["until"] = date_feature.strftime("%Y-%m-%d")
    assert embargo.dump() == embargo_dict


def test_embargo_lift():
    future_date = arrow.utcnow().datetime + timedelta(days=+30)
    past_date = arrow.utcnow().datetime + timedelta(days=-30)
    embargo_dict1 = {"until": future_date, "active": True, "reason": "espionage"}
    embargo_dict2 = {"until": past_date, "active": True, "reason": "espionage"}
    new_embargo = Embargo.from_dict(embargo_dict1)
    old_embargo = Embargo.from_dict(embargo_dict2)

    assert old_embargo._lift()
    assert not old_embargo.active
    assert not new_embargo._lift()
    assert new_embargo.active
