import { commonMandatoryRequestFieldValidation } from "./common_request_attributes.js";

export function mandatorySingleMessageFieldValidation(body) {
    const errorFromCommonFields = commonMandatoryRequestFieldValidation(body, 'Message');

    if (errorFromCommonFields !== null) {
        return errorFromCommonFields
    }

    const { attributes } = body.data

    if (!attributes.messageReference) {
        return [ 400, "Missing messageReference"]
      }

    return null;
}