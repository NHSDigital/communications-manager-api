import {
  duplicateRequestCorrelationId
} from "../config.js";

export function getCorrelationIdError(correlationId) {
  if (correlationId === duplicateRequestCorrelationId) {
    return [
      422,
      "Request exists with identical messageReference",
    ];
  }

  return null;
}
