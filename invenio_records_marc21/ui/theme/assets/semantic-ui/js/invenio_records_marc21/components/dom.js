/*
 * SPDX-FileCopyrightText: 2022-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

export const getInputFromDOM = (elementName) => {
  const element = document.getElementsByName(elementName);
  if (element.length > 0 && element[0].hasAttribute("value")) {
    return JSON.parse(element[0].value);
  }
  return null;
};
