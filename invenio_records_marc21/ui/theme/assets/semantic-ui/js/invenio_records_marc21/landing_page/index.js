// This file is part of Invenio.
//
// Copyright (C) 2021-2024 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

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
