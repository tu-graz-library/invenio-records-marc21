# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Templates models."""

from copy import deepcopy

from invenio_db import db
from invenio_records.models import Timestamp
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy_utils.types import JSONType


class Marc21Templates(db.Model, Timestamp):
    """Represent a base class for record metadata.

    The RecordMetadata object contains a ``created`` and  a ``updated``
    properties that are automatically updated.
    """

    encoder = None
    """"Class-level attribute to set a JSON data encoder/decoder.

    This allows customizing you to e.g. convert specific entries to complex
    Python objects. For instance you could convert ISO-formatted datetime
    objects into Python datetime objects.
    """

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True)

    """Template identifier."""
    values = db.Column(
        db.JSON()
        .with_variant(
            postgresql.JSONB(none_as_null=True),
            "postgresql",
        )
        .with_variant(
            JSONType(),
            "sqlite",
        )
        .with_variant(
            JSONType(),
            "mysql",
        ),
        default=lambda: dict(),
        nullable=True,
    )
    """Store metadata in JSON format.

    When you create a new ``Record`` the ``json`` field value should never be
    ``NULL``. Default value is an empty dict. ``NULL`` value means that the
    record metadata has been deleted.
    """

    active = db.Column(db.Boolean, default=True)
    """Active Template flag."""

    @classmethod
    def create(cls, name: str, data: dict, id_=None, **kwargs):
        """Create a template for Marc21 deposit app.

        :param name: The template name.
        :param data: Template values.
        :returns: The created Template.
        """
        template = cls(id=id_, name=name, data=data)

        db.session.add(template)
        db.session.commit()
        return template

    @classmethod
    def delete(cls, name, force=False):
        """Delete a template from table.

        :param name: The template name.
        :param force: Hard/Soft delete the template.
        :returns: The deleted Template.
        """
        template = cls.get_template(name=name)
        if force:
            db.session.delete(template)
        else:
            template.is_active = False
        db.session.commit()
        return template

    @classmethod
    def deleteall(cls, force):
        """Truncate templates table.

        :param force: Hard/Soft delete all templates.
        :returns: A list of :class:`Marc21Templates` instances.
        """
        if force:
            db.session.query(cls).delete()
        else:
            templates = cls.get_templates()
            for template in templates:
                template.is_active = False
        db.session.commit()

    @classmethod
    def get_template(cls, name):
        """Retrieve multiple templates by id.

        :param names: List of template names.
        :param with_deleted: If `True` then it includes deleted templates.
        :returns: A list of :class:`Marc21Templates` instances.
        """
        with db.session.no_autoflush:
            query = cls.query.filter(cls.name == str(name))
            return query.first()

    @classmethod
    def get_templates(cls, names=None, roles=None, with_deleted=False):
        """Retrieve multiple templates by id.

        :param names: List of template names.
        :param with_deleted: If `True` then it includes deleted templates.
        :returns: A list of :class:`Marc21Templates` instances.
        """
        with db.session.no_autoflush:
            query = cls.query
            query_filters = []
            if names:
                query_filters.append(query.filter(cls.name.in_(names)))
            if with_deleted:
                query_filters.append((cls.is_active != with_deleted))

            all_templates = query.filter(*query_filters).all()
            templates = []
            for template in all_templates:
                if template.data.get("role", "") in roles:
                    templates.append(template)

            return templates

    @hybrid_property
    def is_active(self):
        """Boolean flag to determine if a template is active."""
        return self.active

    @is_active.setter
    def is_active(self, value):
        """Boolean flag to set template as soft deleted."""
        self.active = value

    @property
    def data(self):
        """Get data by decoding the JSON.

        This allows a subclass to override
        """
        return self.decode(self.values)

    @data.setter
    def data(self, value):
        """Set data by encoding the JSON.

        This allows a subclass to override
        """
        self.values = self.encode(value)
        flag_modified(self, "values")

    @classmethod
    def encode(cls, value):
        """Encode a JSON document."""
        data = deepcopy(value)
        return cls.encoder.encode(data) if cls.encoder else data

    @classmethod
    def decode(cls, json):
        """Decode a JSON document."""
        data = deepcopy(json)
        return cls.encoder.decode(data) if cls.encoder else data

    def to_dict(self):
        """Dump the Marc21Template to a dictionary."""
        result_dict = {
            "id": str(self.id),
            "name": str(self.name),
            "active": str(self.active),
            "values": self.data,
            "created_at": self.created,
        }
        return result_dict
