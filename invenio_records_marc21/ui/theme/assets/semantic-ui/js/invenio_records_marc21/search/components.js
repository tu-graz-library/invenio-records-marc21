// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { useState } from "react";
import ReactDOM from "react-dom";
import _camelCase from "lodash/camelCase";
import _truncate from "lodash/truncate";
import {
  Button,
  Card,
  Checkbox,
  Icon,
  Input,
  Item,
  Label,
  List,
} from "semantic-ui-react";
import { BucketAggregation } from "react-searchkit";
import _get from "lodash/get";
import { loadComponents } from "@js/invenio_theme/templates";
import Overridable from "react-overridable";
import { SearchBar, SearchApp } from "@js/invenio_search_ui/components";

export const Marc21RecordResultsListItem = ({ result, index }) => {

  const createdDate = _get(
    result,
    "ui.created",
    "No creation date found."
  );
  
  const publicationDate = _get(
    result,
    "ui.updated",
    "No update date found."
  );
  const access = _get(result, ["ui", "access_status"], []);
  const access_id = _get(access, "id", "public");
  const access_status = _get(access, "title", "Public");
  const access_icon = _get(access, "icon", "unlock");

  const metadata = _get(result, ["ui", "metadata"], []);
  const description = _get(metadata, ["summary", "summary"], "No description");
  const subjects = _get(metadata, "subject_added_entry_topical_term", []);
  
  const publication = _get(metadata, ["production_publication_distribution_manufacture_and_copyright_notice"], []);
  const creators = _get(publication, "name_of_producer_publisher_distributor_manufacturer", []);

  const title = _get(metadata, ["title_statement", "title"], "No title");
  const version = _get(result, "revision_id", null);

  const viewLink = `/marc21/${result.id}`;

  return (
    <Item key={index} href={viewLink}>
      <Item.Content>
        <Item.Extra>
          <div>
            <Label size="tiny" color="blue">
              {publicationDate} {version ? `(${version})` : null}
            </Label>
            <Label size="tiny" className={`access-status ${access_id}`}>
            {access_icon && (
              <i className={`icon ${access_icon}`}></i>
            )}
            {access_status}
            </Label>
            <Button basic floated="right">
              <Icon name="eye" />
              View
            </Button>
          </div>
        </Item.Extra>
        <Item.Header>{title}</Item.Header>
        <Item.Meta>
          {creators.map((creator, index) => (
            <span key={index}>
              {creator}
              {index < creators.length - 1 && ","}
            </span>
          ))}
        </Item.Meta>
        <Item.Description>
          {_truncate(description, { length: 350 })}
        </Item.Description>
        <Item.Extra>
          {subjects.map((subject, index) => (
            <Label key={index} size="tiny">
              {subject.miscellaneous_information}
            </Label>
          ))}
          {createdDate && (
            <div>
              <small>
                Uploaded on <span>{createdDate}</span>
              </small>
            </div>
          )}
        </Item.Extra>
      </Item.Content>
    </Item>
  );
};

export const Marc21RecordResultsGridItem = ({ result, index }) => {
  const metadata = _get(result, ["ui", "metadata", "json"], []);
  const description = _get(metadata, ["summary", "summary"], "No description");
  return (
    <Card fluid key={index} href={`/marc21/${result.pid}`}>
      <Card.Content>
        <Card.Header>{result.metadata.json.title_statement.title}</Card.Header>
        <Card.Description>
          {_truncate(description, { length: 200 })}
        </Card.Description>
      </Card.Content>
    </Card>
  );
};

export const Marc21RecordSearchBarContainer = () => {
  return (
    <Overridable id={"SearchApp.searchbar"}>
      <SearchBar />
    </Overridable>
  );
};

export const Marc21RecordSearchBarElement = ({
  placeholder: passedPlaceholder,
  queryString,
  onInputChange,
  executeSearch,
}) => {
  const placeholder = passedPlaceholder || "Search";
  const onBtnSearchClick = () => {
    executeSearch();
  };
  const onKeyPress = (event) => {
    if (event.key === "Enter") {
      executeSearch();
    }
  };
  return (
    <Input
      action={{
        icon: "search",
        onClick: onBtnSearchClick,
        className: "search",
      }}
      fluid
      placeholder={placeholder}
      onChange={(event, { value }) => {
        onInputChange(value);
      }}
      value={queryString}
      onKeyPress={onKeyPress}
    />
  );
};

export const Marc21RecordFacetsValues = ({
  bucket,
  isSelected,
  onFilterClicked,
  getChildAggCmps,
}) => {
  const childAggCmps = getChildAggCmps(bucket);
  const [isActive, setisActive] = useState(false);
  const hasChildren = childAggCmps && childAggCmps.props.buckets.length > 0;
  const keyField = bucket.key_as_string ? bucket.key_as_string : bucket.key;
  return (
    <List.Item key={bucket.key}>
      <div
        className={`title ${hasChildren ? "" : "facet-subtitle"} ${
          isActive ? "active" : ""
        }`}
      >
        <List.Content floated="right">
          <Label circular>{bucket.doc_count}</Label>
        </List.Content>
        {hasChildren ? (
          <i
            className={`angle ${isActive ? "down" : "right"} icon`}
            onClick={() => setisActive(!isActive)}
          ></i>
        ) : null}
        <Checkbox
          label={bucket.label || keyField}
          value={keyField}
          onClick={() => onFilterClicked(keyField)}
          checked={isSelected}
        />
      </div>
      <div className={`content facet-content ${isActive ? "active" : ""}`}>
        {childAggCmps}
      </div>
    </List.Item>
  );
};

export const Marc21RecordFacets = ({ aggs, currentResultsState }) => {
  return (
    <>
      {aggs.map((agg) => {
        return (
          <div className="ui accordion" key={agg.title}>
            <BucketAggregation title={agg.title} agg={agg} />
          </div>
        );
      })}
    </>
  );
};

export const Marc21BucketAggregationElement = ({ title, containerCmp }) => {
  return (
    <Card className="borderless-facet">
      <Card.Content>
        <Card.Header>{title}</Card.Header>
      </Card.Content>
      <Card.Content>{containerCmp}</Card.Content>
    </Card>
  );
};

export const Marc21ToggleComponent = ({
  updateQueryFilters,
  userSelectionFilters,
  filterValue,
  label,
  title,
  isChecked,
}) => {
  const _isChecked = (userSelectionFilters) => {
    const isFilterActive =
      userSelectionFilters.filter((filter) => filter[0] === filterValue[0])
        .length > 0;
    return isFilterActive;
  };

  const onToggleClicked = () => {
    updateQueryFilters(filterValue);
  };

  var isChecked = _isChecked(userSelectionFilters);
  return (
    <Card className="borderless-facet">
      <Card.Content>
        <Card.Header>{title}</Card.Header>
      </Card.Content>
      <Card.Content>
        <Checkbox
          toggle
          label={label}
          onClick={onToggleClicked}
          checked={isChecked}
        />
      </Card.Content>
    </Card>
  );
};

export const Marc21CountComponent = ({ totalResults }) => {
  return <Label>{totalResults.toLocaleString("en-US")}</Label>;
};


export function createMarc21SearchAppInit(
  defaultComponents,
  autoInit = true,
  autoInitDataAttr = "invenio-records-marc21-search-config"
) {
  const initSearchApp = (rootElement) => {
    const config = JSON.parse(
      rootElement.dataset[_camelCase(autoInitDataAttr)]
    );
    loadComponents(config.appId, defaultComponents).then((res) => {
      ReactDOM.render(<SearchApp config={config} />, rootElement);
    });
  };

  if (autoInit) {
    const searchAppElements = document.querySelectorAll(
      `[data-${autoInitDataAttr}]`
    );
    for (const appRootElement of searchAppElements) {
      initSearchApp(appRootElement);
    }
  } else {
    return initSearchApp;
  }
}