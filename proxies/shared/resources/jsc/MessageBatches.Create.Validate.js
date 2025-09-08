/**
 * This script validates the data in the body of a POST request to the /v1/message-batches endpoint, returning an
 * array of up to 100 error responses to be returned by Apigee as a 400 error response.
 *
 * It is called by the JavaScript.MessageBatches.Create.Validate policy.
 */

var content = context.getVariable("request.content")
var errors = []

var all
try {
  all = JSON.parse(content)
} catch (e) {
  errors.push(invalidError("/"))
}


const validate = () => {
  if (all) {
    var seenMessages = {};
    var data = all.data;

    const validDataObject = validateObject(errors, data, "/data")
    if (validDataObject) {
      validateConstantString(errors, data.type, "/data/type", "MessageBatch")

      const validAttributesObject = validateObject(errors, data.attributes, "/data/attributes")
      if (validAttributesObject) {

        validateUuid(errors, data.attributes.routingPlanId, "/data/attributes/routingPlanId")

        validateString(errors, data.attributes.messageBatchReference, "/data/attributes/messageBatchReference")

        const validArray = validateArray(errors, data.attributes.messages, "/data/attributes/messages", 1)
        if (validArray) {
          if (data.attributes.messages.length > 45000) {
            errors.push(tooManyItemsError("/data/attributes/messages"));
            return null;
          }
          data.attributes.messages.forEach((message, index) => {
            var pointer = "/data/attributes/messages/" + index;
            // Limit the amount of errors returned to 100 entries
            if (errors.length >= 100) {
              errors = errors.slice(0, 100);
              return null;
            }

            if (isUndefined(message)) {
              errors.push(missingError(pointer));
            } else if (message === null) {
              errors.push(nullError(pointer));
            } else if (typeof message !== "object" || Array.isArray(message)) {
              errors.push(invalidError(pointer));
            } else {

              pointer = "/data/attributes/messages/" + index + "/messageReference";
              const validMessageReference = validateString(errors, message.messageReference, pointer)
              if (validMessageReference) {
                if (seenMessages[message.messageReference]) {
                  errors.push(duplicateError(pointer));
                } else {
                  seenMessages[message.messageReference] = 1;
                }
              }

              const validRecipientObject = validateObject(errors, message.recipient, "/data/attributes/messages/" + index + "/recipient")
              if (validRecipientObject) {

                validateNhsNumber(errors, message.recipient.nhsNumber, "/data/attributes/messages/" + index + "/recipient/nhsNumber")
              }

              if (!isUndefined(message.originator)) {
                const validOriginatorObject = validateObject(errors, message.originator, "/data/attributes/messages/" + index + "/originator")
                if (validOriginatorObject) {
                  validateOdsCode(errors, message.originator.odsCode, "/data/attributes/messages/" + index + "/originator/odsCode")
                }
              }

              pointer = "/data/attributes/messages/" + index + "/personalisation";
              if (!isUndefined(message.personalisation)) {
                validateObject(errors, message.personalisation, pointer)
              }
            }
          });
        }
      }
    }
  }
}

validate();

if (errors.length > 0) {
  context.setVariable("generic_status_code", errors[0].status);
  context.setVariable("errors", JSON.stringify(errors));
} else {
  context.setVariable("generic_status_code", null);
  context.setVariable("errors", null);
}
