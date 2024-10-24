// This file is part of Invenio.
//
// Copyright (C) 2020-2021 CERN.
// Copyright (C) 2020-2021 Northwestern University.
// Copyright (C) 2021-2024 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { useState } from "react";
import { Grid, Icon } from "semantic-ui-react";
import { EditButton } from "../components/EditButton";
import { NewVersionButton } from "@js/invenio_rdm_records";
import { i18next } from "@translations/invenio_records_marc21/i18next";

export const RecordManagement = (props) => {
  const record = props.record;
  const recid = record.id;
  const permissions = props.permissions;
  const [error, setError] = useState("");
  const handleError = (errorMessage) => {
    console.log(errorMessage);
    setError(errorMessage);
  };

  return (
    <Grid relaxed>
      <Grid.Column>
        <Grid.Row>
          <Icon name="cogs" />
          <span>{i18next.t("Manage")}</span>
        </Grid.Row>
        <Grid.Row className="record-management-row">
          <EditButton
            fluid
            className="warning"
            size="medium"
            recid={recid}
            onError={handleError}
          />
          <NewVersionButton
            record={record}
            onError={handleError}
            disabled={!permissions.can_new_version}
          />
        </Grid.Row>
        {error && (
          <Grid.Row className="record-management-row">
            <p>{error}</p>
          </Grid.Row>
        )}
      </Grid.Column>
    </Grid>
  );
};
