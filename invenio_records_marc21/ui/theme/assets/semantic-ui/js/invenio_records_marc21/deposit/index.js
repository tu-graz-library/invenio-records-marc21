/*
 * SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import React from "react";
import ReactDOM from "react-dom";

import { getInputFromDOM } from "@js/invenio_rdm_records";
import { Marc21DepositForm } from "./Marc21DepositForm";

ReactDOM.render(
  <Marc21DepositForm
    record={getInputFromDOM("marc21-deposit-record")}
    files={getInputFromDOM("marc21-deposit-files")}
    config={getInputFromDOM("marc21-deposit-config")}
    templates={getInputFromDOM("marc21-deposit-templates")}
    permissions={getInputFromDOM("marc21-deposit-permissions")}
  />,
  document.getElementById("marc21-deposit-form"),
);
