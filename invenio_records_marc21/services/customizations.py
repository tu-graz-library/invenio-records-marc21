# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2022 Northwestern University.
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Helpers for customizing the configuration in a controlled manner."""


# TODO:
# NOTE:
# copy pasted code from invenio_rdm_records/services/customizations.py
class FromConfigPIDsProviders:
    """Data descriptor for pid providers configuration."""

    def __init__(self, persistent_identifiers, persistent_identifier_providers):
        """Constructor for FromConfigPIDsProviders."""
        self.persistent_identifiers = persistent_identifiers
        self.persistent_identifier_providers = persistent_identifier_providers

    def __get__(self, obj, objtype=None):
        """Return value that was grafted on obj (descriptor protocol)."""

        def get_provider_dict(pid_config, pid_providers):
            """Return pid provider dict in shape expected by config users.

            (This transformation would be unnecesary if the pid_providers were
            in the right shape already).
            """
            provider_dict = {"default": None}

            for name in pid_config.get("providers", []):
                # This may throw a KeyError which is a sign that the config
                # is wrong.
                provider_dict[name] = pid_providers[name]
                provider_dict["default"] = provider_dict["default"] or name

            return provider_dict

        pids = obj._app.config.get(self.persistent_identifiers, {})
        providers = {
            p.name: p
            for p in obj._app.config.get(self.persistent_identifier_providers, [])
        }
        doi_enabled = obj._app.config.get("DATACITE_ENABLED", False)

        return {
            scheme: get_provider_dict(conf, providers)
            for scheme, conf in pids.items()
            if scheme != "doi" or doi_enabled
        }


# TODO:
# NOTE:
# copy pasted code from invenio_rdm_records/services/customizations.py
class FromConfigRequiredPIDs:
    """Data descriptor for required pids configuration."""

    def __init__(self, persistent_identifiers):
        """Constructor for FomConfigRequiredPIDS."""
        self.persistent_identifiers = persistent_identifiers

    def __get__(self, obj, objtype=None):
        """Return required pids (descriptor protocol)."""
        pids = obj._app.config.get(self.persistent_identifiers, {})
        doi_enabled = obj._app.config.get("DATACITE_ENABLED", False)

        pids = {
            scheme: conf
            for (scheme, conf) in pids.items()
            if scheme != "doi" or doi_enabled
        }
        return [
            scheme for (scheme, conf) in pids.items() if conf.get("required", False)
        ]
