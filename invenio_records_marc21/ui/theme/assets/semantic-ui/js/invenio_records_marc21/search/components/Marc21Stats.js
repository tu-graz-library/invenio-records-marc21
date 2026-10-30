/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

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
