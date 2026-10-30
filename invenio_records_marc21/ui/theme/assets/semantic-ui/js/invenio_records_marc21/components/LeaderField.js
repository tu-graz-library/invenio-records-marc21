/*
 * SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import React, { Component } from "react";
import PropTypes from "prop-types";

import { TextField } from "react-invenio-forms";

export class LeaderField extends Component {
  render() {
    const { fieldPath } = this.props;
    return (
      <>
        <TextField
          fieldPath="ldr"
          value="LDR"
          width={3}
          className="key narrow"
          disabled
        />
        <TextField
          fieldPath={`${fieldPath}`}
          width={15}
          required
          maxLength={24}
          className="narrow"
        />
      </>
    );
  }
}

LeaderField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};
