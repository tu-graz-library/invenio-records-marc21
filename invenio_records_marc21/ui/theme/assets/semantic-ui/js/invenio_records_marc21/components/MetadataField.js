// This file is part of Invenio.
//
// Copyright (C) 2021-2022 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { Component } from "react";
import PropTypes from "prop-types";

import { TextField } from "react-invenio-forms";

export class MetadataField extends Component {
  render() {
    const { fieldPath } = this.props;
    return (
      <>
        <TextField
          fieldPath={`${fieldPath}.id`}
          width={2}
          required
          maxLength={3}
          className={"key narrow"}
        />
        <TextField
          fieldPath={`${fieldPath}.ind1`}
          width={1}
          maxLength={1}
          className={"ind1 narrow"}
        />
        <TextField
          fieldPath={`${fieldPath}.ind2`}
          width={1}
          maxLength={1}
          className={"ind2 narrow"}
        />
        <TextField
          fieldPath={`${fieldPath}.subfield`}
          width={15}
          required
          className={"narrow"}
        />
      </>
    );
  }
}

MetadataField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  width: PropTypes.number,
  helpText: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
};

MetadataField.defaultProps = {
  helpText: "",
};
