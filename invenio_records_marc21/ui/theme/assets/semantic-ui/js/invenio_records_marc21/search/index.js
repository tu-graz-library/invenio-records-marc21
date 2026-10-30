/*
 * SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import { parametrize } from "react-overridable";
import { createSearchAppInit } from "@js/invenio_search_ui";
import {
  RDMRecordSearchBarContainer,
  RDMRecordMultipleSearchBarElement,
  RDMToggleComponent,
  RDMCountComponent,
  RDMErrorComponent,
  RDMEmptyResults,
} from "@js/invenio_app_rdm/search/components";
import {
  ContribSearchAppFacets,
  ContribBucketAggregationElement,
  ContribBucketAggregationValuesElement,
} from "@js/invenio_search_ui/components";
import {
  Marc21RecordResultsGridItem,
  Marc21RecordResultsListItem,
} from "./components";

const ContribSearchAppFacetsWithConfig = parametrize(ContribSearchAppFacets, {
  toogle: true,
});

export const Marc21EmptyResults = parametrize(RDMEmptyResults, {
  searchPath: "/publications/search",
});

const initSearchApp = createSearchAppInit({
  "BucketAggregation.element": ContribBucketAggregationElement,
  "BucketAggregationValues.element": ContribBucketAggregationValuesElement,
  "EmptyResults.element": Marc21EmptyResults,
  "ResultsGrid.item": Marc21RecordResultsGridItem,
  "ResultsList.item": Marc21RecordResultsListItem,
  "SearchApp.facets": ContribSearchAppFacetsWithConfig,
  "SearchApp.searchbarContainer": RDMRecordSearchBarContainer,
  "SearchBar.element": RDMRecordMultipleSearchBarElement,
  "SearchFilters.ToggleComponent": RDMToggleComponent,
  "Error.element": RDMErrorComponent,
  "Count.element": RDMCountComponent,
  "SearchFilters.Toggle.element": RDMToggleComponent,
});
