/**
 * This script validates the data in the body of a POST request to the /v1/message-batches endpoint, returning an
 * array of up to 100 error responses to be returned by Apigee as a 400 error response.
 *
 * It is called by the JavaScript.MessageBatches.Create.Validate policy.
 */

// Regex to validate the id is a valid UUID
const uuidRegex = /^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$/i
const nhsNumberRegex = /^\d{10}$/i
const dobRegex = /^\d{4}-\d{2}-\d{2}$/i
const messageId = context.getVariable("messageid");

var content = context.getVariable("request.content")
var errors = []

var all
try {
  all = JSON.parse(content)
} catch(e) {
  pushError(invalidError("/"))
}

const isUndefined = (val) => {
    return typeof val === "undefined";
}

const isValidNhsNumber = (nhsNumber, nhsNumberRegex) => {
  if (!nhsNumberRegex.test(nhsNumber)) {
    return false;
  }

  const checkDigit = nhsNumber.substring(9);

  var total = 0;
  for (var i = 0; i <= 8; i++) {
    var digit = (parseInt(nhsNumber.substring(i, i+1)))
    total += (digit * (10 - i))
  }

  const remainder = total % 11;
  return (11 - remainder) % 11 === parseInt(checkDigit);
}


const validate = () => {
  if (all) {
    var seenMessages = {};
    var data = all.data;

    var pointer;

    // $.data
    pointer = "/data";
    if (isUndefined(data)) {
      pushError(missingError(pointer));
    } else if (data === null) {
      pushError(nullError(pointer));
    } else if (typeof data !== "object") {
      pushError(invalidError(pointer));
    } else {

      // $.data.type
      pointer = "/data/type";
      if (isUndefined(data.type)) {
        pushError(missingError(pointer));
      } else if (data.type === null) {
        pushError(nullError(pointer));
      } else if (data.type !== "MessageBatch") {
        pushError(invalidError(pointer));
      }

      // $.data.attributes
      pointer = "/data/attributes";
      if (isUndefined(data.attributes)) {
        pushError(missingError(pointer));
      } else if (data.attributes === null) {
        pushError(nullError(pointer));
      } else if (typeof data.attributes !== "object") {
        pushError(invalidError(pointer));
      } else {

        // $.data.attributes.routingPlanId
        pointer = "/data/attributes/routingPlanId";
        if (isUndefined(data.attributes.routingPlanId)) {
          pushError(missingError(pointer));
        } else if (data.attributes.routingPlanId === null) {
          pushError(nullError(pointer));
        } else if (typeof data.attributes.routingPlanId !== "string" || !uuidRegex.test(data.attributes.routingPlanId)) {
          pushError(invalidError(pointer));
        }

        // $.data.attributes.messageBatchReference
        pointer = "/data/attributes/messageBatchReference";
        if (isUndefined(data.attributes.messageBatchReference)) {
          pushError(missingError(pointer));
        } else if (data.attributes.messageBatchReference === null) {
          pushError(nullError(pointer));
        } else if (typeof data.attributes.messageBatchReference !== "string" || !uuidRegex.test(data.attributes.messageBatchReference)) {
          pushError(invalidError(pointer));
        }

        // $.data.attributes.messages
        pointer = "/data/attributes/messages";
        if (isUndefined(data.attributes.messages)) {
          pushError(missingError(pointer));
        } else if (data.attributes.messages === null) {
          pushError(nullError(pointer));
        } else if (!Array.isArray(data.attributes.messages)) {
          pushError(invalidError(pointer));
        } else if (data.attributes.messages.length === 0) {
          pushError(tooFewItemsError(pointer));
        } else {

          // $.data.attributes.messages.x
          data.attributes.messages.forEach((message, index) => {
            pointer = "/data/attributes/messages/" + index;
            // Limit the amount of errors returned to 100 entries
            if (errors.length >= 100) {
              errors = errors.slice(0, 100);
              return null;
            }

            if (isUndefined(message)) {
              pushError(missingError(pointer));
            } else if (message === null) {
              pushError(nullError(pointer));
            } else if (typeof message !== "object" || Array.isArray(message)) {
              pushError(invalidError(pointer));
            } else {

              // $.data.attributes.messages.x.messageReference
              pointer = "/data/attributes/messages/" + index + "/messageReference";
              if (isUndefined(message.messageReference)) {
                pushError(missingError(pointer));
              } else if (message.messageReference === null) {
                pushError(nullError(pointer));
              } else if (typeof message.messageReference !== "string" || !uuidRegex.test(message.messageReference)) {
                pushError(invalidError(pointer));
              } else if (seenMessages[message.messageReference]) {
                pushError(duplicateError(pointer));
              } else {
                seenMessages[message.messageReference] = 1;
              }

              // $.data.attributes.messages.x.recipient
              pointer = "/data/attributes/messages/" + index + "/recipient";
              if (isUndefined(message.recipient)) {
                pushError(missingError(pointer));
              } else if (typeof message.recipient !== 'object') {
                pushError(invalidError(pointer));
              } else if (message.recipient === null) {
                pushError(nullError(pointer));
              } else {

                // $.data.attributes.messages.x.recipient.nhsNumber
                pointer = "/data/attributes/messages/" + index + "/recipient/nhsNumber";
                if (isUndefined(message.recipient.nhsNumber)) {
                  pushError(missingError(pointer));
                } else if (message.recipient.nhsNumber === null) {
                  pushError(nullError(pointer));
                } else if (typeof message.recipient.nhsNumber !== "string" || !isValidNhsNumber(message.recipient.nhsNumber, nhsNumberRegex)) {
                  pushError(invalidNhsNumberError(pointer));
                }

                // $.data.attributes.recipients.x.dateOfBirth
                pointer = "/data/attributes/messages/" + index + "/recipient/dateOfBirth";
                if (
                  !isUndefined(message.recipient.dateOfBirth)
                  && (
                    message.recipient.dateOfBirth === null
                    || typeof message.recipient.dateOfBirth !== "string"
                    || !dobRegex.test(message.recipient.dateOfBirth)
                  )
                ) {
                  pushError(invalidError(pointer));
                }

                // $.data.attributes.messages.x.personalisation
                pointer = "/data/attributes/messages/" + index + "/personalisation";
                if (!isUndefined(message.personalisation) && typeof message.personalisation !== "object") {
                  pushError(invalidError(pointer));
                }
              }
            }
          });
        }
      }
    }
  }
}

function pushError(error) {
  errors.push(error);
}

function createErrorObject(code, title, detail, pointer, links) {
  return {
    "id" : messageId + "." + errors.length,
    "code": code,
    "links": Object.assign({}, {"about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"}, links),
    "status": "400",
    "title": title,
    "detail": detail,
    "source": {
      "pointer": pointer
    }
  };
}

function missingError(pointer) {
  return createErrorObject(
    "CM_MISSING_VALUE",
    "Missing property",
    "The property at the specified location is required, but was not present in the request.",
    pointer,
    {}
  );
}

function nullError(pointer) {
  return createErrorObject(
    "CM_NULL_VALUE",
    "Property cannot be null",
    "The property at the specified location is required, but a null value was passed in the request.",
    pointer,
    {}
  );
}

function invalidError(pointer) {
  return createErrorObject(
    "CM_INVALID_VALUE",
    "Invalid value",
    "The property at the specified location does not allow this value.",
    pointer,
    {}
  );
}

function duplicateError(pointer) {
  return createErrorObject(
    "CM_DUPLICATE_VALUE",
    "Duplicate value",
    "The property at the specified location is a duplicate, duplicated values are not allowed.",
    pointer,
    {}
  );
}

function tooFewItemsError(pointer) {
  return createErrorObject(
    "CM_TOO_FEW_ITEMS",
    "Too few items",
    "The property at the specified location contains too few items.",
    pointer,
    {}
  )
}

function invalidNhsNumberError(pointer) {
  return createErrorObject(
    "CM_INVALID_NHS_NUMBER",
    "Invalid nhs number",
    "The value provided in this nhsNumber field is not a valid NHS number.",
    pointer,
    {"nhsNumbers": "https://www.datadictionary.nhs.uk/attributes/nhs_number.html"}
  );
}

validate();

if (errors.length > 0) {
  context.setVariable("errors", JSON.stringify(errors));
} else {
  context.setVariable("errors", null);
}
