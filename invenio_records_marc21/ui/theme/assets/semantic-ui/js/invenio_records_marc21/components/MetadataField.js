/*
 * SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

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
          className="key narrow"
        />
        <TextField
          fieldPath={`${fieldPath}.ind1`}
          width={1}
          maxLength={1}
          className="ind1 narrow"
        />
        <TextField
          fieldPath={`${fieldPath}.ind2`}
          width={1}
          maxLength={1}
          className="ind2 narrow"
        />
        <TextField
          fieldPath={`${fieldPath}.subfield`}
          width={15}
          required
          className="narrow"
        />
      </>
    );
  }
}

MetadataField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};
