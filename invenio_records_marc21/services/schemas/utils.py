# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record schema utilities."""

# from marshmallow import Schema, ValidationError, fields
# from marshmallow.schema import SchemaMeta
# from marshmallow_utils.fields import NestedAttribute

# from ...vocabularies import Vocabularies


# def validate_entry(vocabulary_key, entry_key):
#     """Validates if an entry is valid for a vocabulary.

#     :param vocabulary_key: str, Vocabulary key
#     :param entry_key: str, specific entry key

#     raises marshmallow.ValidationError if entry is not valid.
#     """
#     vocabulary = Vocabularies.get_vocabulary(vocabulary_key)
#     obj = vocabulary.get_entry_by_dict(entry_key)
#     if not obj:
#         raise ValidationError(vocabulary.get_invalid(entry_key))
