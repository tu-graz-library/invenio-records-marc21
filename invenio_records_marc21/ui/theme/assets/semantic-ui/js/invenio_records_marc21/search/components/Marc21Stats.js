// This file is part of Invenio.
//
// Copyright (C) 2024 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import PropTypes from "prop-types";
import React from "react";
import { Icon, Label, Popup } from "semantic-ui-react";
import { i18next } from "@translations/invenio_records_marc21/i18next";

export const Marc21Stats = ({ uniqueViews, uniqueDownloads }) => {
  return (
    <>
      {uniqueViews != null && (
        <Popup
          size="tiny"
          content={i18next.t("Views")}
          trigger={
            <Label className="transparent">
              <Icon name="eye" />
              {uniqueViews}
            </Label>
          }
        />
      )}
      {uniqueDownloads != null && (
        <Popup
          size="tiny"
          content={i18next.t("Downloads")}
          trigger={
            <Label className="transparent">
              <Icon name="download" />
              {uniqueDownloads}
            </Label>
          }
        />
      )}
    </>
  );
};

Marc21Stats.propTypes = {
  uniqueViews: PropTypes.number,
  uniqueDownloads: PropTypes.number,
};

Marc21Stats.defaultProps = {
  uniqueViews: null,
  uniqueDownloads: null,
};
