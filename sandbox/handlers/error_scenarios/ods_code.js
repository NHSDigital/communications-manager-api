import {
  noDefaultOdsClientAuth,
  noOdsChangeClientAuth,
} from "../config.js"

export function getOdsCodeError(odsCode, authorizationHeader) {
  if (!odsCode && authorizationHeader === noDefaultOdsClientAuth) {
    return [
      400,
      'odsCode must be provided'
    ]
  }

  if (odsCode && authorizationHeader === noOdsChangeClientAuth) {
    return [
      400,
      'odsCode was provided but ODS code override is not enabled for the client'
    ]
  }
  return null;
}