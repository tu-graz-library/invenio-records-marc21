/*
 * SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";
import { ExportDropdown } from "@js/invenio_app_rdm/landing_page/ExportDropdown";

const recordExportDownloadDiv = document.getElementById("recordExportDownload");

if (recordExportDownloadDiv) {
  ReactDOM.render(
    <ExportDropdown
      formats={JSON.parse(recordExportDownloadDiv.dataset.formats)}
    />,
    recordExportDownloadDiv
  );
}

$("#record-doi-badge").on("click", function () {
  $("#doi-modal").modal("show");
});
