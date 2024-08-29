import { commonMandatoryRequestFieldValidation} from "./common_request_attributes.js";

export function mandatoryBatchMessageFieldValidation(body) {
    const errorFromCommonFields = commonMandatoryRequestFieldValidation(body, 'MessageBatch');

    if (errorFromCommonFields !== null) {
        return errorFromCommonFields
    }

    const { attributes } = body.data

    if (!attributes.messageBatchReference) {
        return [ 400, "Missing messageBatchReference"]

      }
    
      if (!Array.isArray(attributes.messages)) {
        return [ 400, "Missing messages array"]
      }
    
      const messageReferences = attributes.messages.map((message) => message.messageReference);
      if (messageReferences.includes(undefined)) {
        return [400, "Missing messageReferences"]
      }
    
      if (new Set(messageReferences).size !== messageReferences.length) {
        return [400, "Duplicate messageReferences"]
      }

    return null;
}