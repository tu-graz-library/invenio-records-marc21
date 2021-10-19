// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.


import { createSearchAppInit } from "@js/invenio_search_ui";
import {
  Marc21BucketAggregationElement,
  Marc21RecordFacets,
  Marc21RecordFacetsValues,
  Marc21RecordResultsGridItem,
  Marc21RecordResultsListItem,
  Marc21RecordSearchBarContainer,
  Marc21RecordSearchBarElement,
  Marc21ToggleComponent,
  Marc21CountComponent,
} from "./components";


const initSearchApp = createSearchAppInit({
  "BucketAggregation.element": Marc21BucketAggregationElement,
  "BucketAggregationValues.element": Marc21RecordFacetsValues,
  "ResultsGrid.item": Marc21RecordResultsGridItem,
  "ResultsList.item": Marc21RecordResultsListItem,
  "SearchApp.facets": Marc21RecordFacets,
  "SearchApp.searchbarContainer": Marc21RecordSearchBarContainer,
  "SearchBar.element": Marc21RecordSearchBarElement,
  "SearchFilters.ToggleComponent": Marc21ToggleComponent,
  "Count.element": Marc21CountComponent,
});
