// This file is part of Invenio.
//
// Copyright (C) 2023 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React from "react";
import { parametrize } from "react-overridable";
import { createSearchAppInit } from "@js/invenio_search_ui";
import { Button, Divider, Header, Segment } from "semantic-ui-react";
import {
  RDMRecordSearchBarContainer,
  RDMRecordSearchBarElement,
  RDMToggleComponent,
  RDMCountComponent,
  RDMErrorComponent,
} from "@js/invenio_app_rdm/search/components";
import {
  ContribSearchAppFacets,
  ContribBucketAggregationElement,
  ContribBucketAggregationValuesElement,
} from "@js/invenio_search_ui/components";
import {
  Marc21RecordResultsGridItem,
  Marc21RecordResultsListItem,
} from "@js/invenio_records_marc21/search/components";
import { i18next } from "@translations/invenio_records_marc21/i18next";
import {
  DashboardSearchLayoutHOC,
  DashboardResultView,
} from "@js/invenio_app_rdm/user_dashboard/base";

const ContribSearchAppFacetsWithConfig = parametrize(ContribSearchAppFacets, {
  toogle: true,
});

const Marc21RecordResultsListItemWithConfig = parametrize(
  Marc21RecordResultsListItem,
  {
    dashboard: true, // show view and edit buttons in the result item
  }
);
export const Marc21SearchLayout = DashboardSearchLayoutHOC({
  searchBarPlaceholder: i18next.t("Search in publications..."),
});

export const Marc21EmptyResults = (props) => {
  return (
    <Segment.Group>
      <Segment placeholder textAlign="center" padded="very">
        <Header as="h1" align="center">
          <Header.Content>
            <Header.Subheader>
              {i18next.t("Make your first upload!")}
            </Header.Subheader>
          </Header.Content>
        </Header>
        <Divider hidden />
        <Button
          positive
          icon="upload"
          floated="right"
          href="/publications/uploads/new"
          content={i18next.t("New upload")}
        />
      </Segment>
    </Segment.Group>
  );
};

const initSearchApp = createSearchAppInit({
  "BucketAggregation.element": ContribBucketAggregationElement,
  "BucketAggregationValues.element": ContribBucketAggregationValuesElement,
  "EmptyResults.element": Marc21EmptyResults,
  "ResultsGrid.item": Marc21RecordResultsGridItem,
  "ResultsList.item": Marc21RecordResultsListItemWithConfig,
  "SearchApp.facets": ContribSearchAppFacetsWithConfig,
  "SearchApp.searchbarContainer": RDMRecordSearchBarContainer,
  "SearchBar.element": RDMRecordSearchBarElement,
  "SearchApp.layout": Marc21SearchLayout,
  "SearchApp.results": DashboardResultView,
  "SearchFilters.ToggleComponent": RDMToggleComponent,
  "Error.element": RDMErrorComponent,
  "Count.element": RDMCountComponent,
  "SearchFilters.Toggle.element": RDMToggleComponent,
});
