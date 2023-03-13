// This file is part of Invenio.
//
// Copyright (C) 2021 Northwestern University.
// Copyright (C) 2021-2023 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { useState } from "react";
import { Button } from "semantic-ui-react";
import { http } from "react-invenio-forms";
import PropTypes from "prop-types";
import { i18next } from "@translations/invenio_records_marc21/i18next";

export const EditButton = ({ recid, onError }) => {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      await http.post(`/api/marc21/${recid}/draft`);
      window.location = `/marc21/uploads/${recid}`;
    } catch (error) {
      setLoading(false);
      onError(error.response.data.message);
    }
  };

  return (
    <Button
      compact
      size="small"
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
