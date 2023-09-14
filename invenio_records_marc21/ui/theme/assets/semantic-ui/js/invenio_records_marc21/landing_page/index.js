// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";

import { RecordManagement } from "./Marc21RecordManagement";
import { RecordVersionsList } from "./Marc21RecordVersionsList";
import { ExportDropdown } from "@js/invenio_app_rdm/landing_page/ExportDropdown";

const recordManagementAppDiv = document.getElementById("recordManagement");
const recordVersionsAppDiv = document.getElementById("recordVersions");
const recordExportDownloadDiv = document.getElementById("recordExportDownload");

if (recordManagementAppDiv) {
  ReactDOM.render(
    <RecordManagement
      record={JSON.parse(recordManagementAppDiv.dataset.record)}
      permissions={JSON.parse(recordManagementAppDiv.dataset.permissions)}
    />,
    recordManagementAppDiv
  );
}

if (recordVersionsAppDiv) {
  ReactDOM.render(
    <RecordVersionsList
      record={JSON.parse(recordVersionsAppDiv.dataset.record)}
      isPreview={JSON.parse(recordVersionsAppDiv.dataset.preview)}
    />,
    recordVersionsAppDiv
  );
}

if (recordExportDownloadDiv) {
  ReactDOM.render(
    <ExportDropdown
      formats={JSON.parse(recordExportDownloadDiv.dataset.formats)}
    />,
    recordExportDownloadDiv
  );
}

$(".ui.accordion").accordion({
  selector: {
    trigger: ".title .dropdown",
  },
});

$(".ui.tooltip-popup").popup();

$(".preview-link").on("click", function (event) {
  $("#preview").find(".title").html(event.target.dataset.fileKey);
});

$("#jump-btn").on("click", function (event) {
  document.documentElement.scrollTop = 0;
});

// func to toggle the icon class
$(".panel-heading").click(function () {
  $("i", this).toggleClass("down right");
});

$("#record-doi-badge").on("click", function () {
  $("#doi-modal").modal("show");
});
