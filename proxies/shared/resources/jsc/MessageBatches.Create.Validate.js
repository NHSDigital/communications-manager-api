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

    // $.data
    const validDataObject = validateObject(errors, data, "/data")
    if (validDataObject) {
      // $.data.type
      validateConstantString(errors, data.type, "/data/type", "MessageBatch")

      // $.data.attributes
      const validAttributesObject = validateObject(errors, data.attributes, "/data/attributes")
      if (validAttributesObject) {


        // $.data.attributes.routingPlanId
        validateUuid(errors, data.attributes.routingPlanId, "/data/attributes/routingPlanId")

        // $.data.attributes.messageBatchReference
        validateUuid(errors, data.attributes.messageBatchReference, "/data/attributes/messageBatchReference")

        // $.data.attributes.messages
        const validArray = validateArray(errors, data.attributes.messages, "/data/attributes/messages", 1)
        if (validArray) {
          if (data.attributes.messages.length > 45000) {
            errors.push(tooManyItemsError("/data/attributes/messages"));
          }
          // $.data.attributes.messages.x
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

              // $.data.attributes.messages.x.messageReference
              pointer = "/data/attributes/messages/" + index + "/messageReference"
              const validMessageReferenceUuid = validateUuid(errors, message.messageReference, pointer)
              if (validMessageReferenceUuid) {
                if (seenMessages[message.messageReference]) {
                  errors.push(duplicateError(pointer));
                } else {
                  seenMessages[message.messageReference] = 1;
                }
              }

              // $.data.attributes.messages.x.recipient
              const validRecipientObject = validateObject(errors, message.recipient, "/data/attributes/messages/" + index + "/recipient")
              if (validRecipientObject) {

                // $.data.attributes.messages.x.recipient.nhsNumber
                validateNhsNumber(errors, message.recipient.nhsNumber, "/data/attributes/messages/" + index + "/recipient/nhsNumber")

                // $.data.attributes.recipients.x.dateOfBirth
                validateDob(errors, message.recipient.dateOfBirth, "/data/attributes/messages/" + index + "/recipient/dateOfBirth")

              }

              if (!isUndefined(message.originator)) {
                // $.data.attributes.messages.x.originator
                const validOriginatorObject = validateObject(errors, message.originator, "/data/attributes/messages/" + index + "/originator")
                if (validOriginatorObject) {
                  // $.data.attributes.messages.x.originator.odsCode
                  validateOdsCode(errors, message.originator.odsCode, "/data/attributes/messages/" + index + "/originator/odsCode")
                }
              }

              // $.data.attributes.messages.x.personalisation
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
  context.setVariable("errors", JSON.stringify(errors));
} else {
  context.setVariable("errors", null);
}
