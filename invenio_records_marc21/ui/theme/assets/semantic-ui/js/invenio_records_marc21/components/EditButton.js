/*
 * SPDX-FileCopyrightText: 2021 Northwestern University.
 * SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import React, { useState } from "react";
import { Button } from "semantic-ui-react";
import { http } from "react-invenio-forms";
import PropTypes from "prop-types";
import { i18next } from "@translations/invenio_records_marc21/i18next";

export const EditButton = ({
  recid,
  onError,
  linkLocation,
  linkEdit,
  className,
  size,
  fluid,
}) => {
  const [loading, setLoading] = useState(false);

  size = size || "small";
  fluid = fluid || false;

  const handleClick = async () => {
    setLoading(true);
    try {
      await http.post(
        linkEdit,
        {},
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/vnd.inveniomarc21.v1+json",
          },
        },
      );
      window.location = linkLocation;
    } catch (error) {
      setLoading(false);
      onError(error.response.data.message);
    }
  };

  return (
    <Button
      compact
      fluid={fluid}
      className={className}
      size={size}
      floated="right"
      onClick={() => handleClick()}
      icon="edit"
      content={i18next.t("Edit")}
    />
  );
};

EditButton.propTypes = {
  recid: PropTypes.string.isRequired,
  onError: PropTypes.object.isRequired,
};
