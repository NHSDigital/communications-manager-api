// Regex to validate the id is a valid UUID
const uuidRegex = /^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$/i
const nhsNumberRegex = /^[0-9]{10}$/i
const dobRegex = /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/i

var content = context.getVariable("request.content")
var errors = []

var all
try {
  all = JSON.parse(content)
} catch(e) {
  pushError(invalidError("/"))
}

if (all) {
  var seenMessages = []
  var data = all.data;

  var pointer

  // $.data
  pointer = "/data"
  if (typeof data === "undefined") {
    pushError(missingError(pointer))
  } else if (data === null) {
    pushError(nullError(pointer))
  } else if (typeof data !== "object") {
    pushError(invalidError(pointer))
  } else {

    // $.data.type
    pointer = "/data/type"
    if (typeof data.type === "undefined") {
      pushError(missingError(pointer))
    } else if (data.type === null) {
      pushError(nullError(pointer))
    } else if (data.type !== "MessageBatch") {
      pushError(invalidError(pointer))
    }

    // $.data.attributes
    pointer = "/data/attributes"
    if (typeof data.attributes === "undefined") {
      pushError(missingError(pointer))
    } else if (data.attributes === null) {
      pushError(nullError(pointer))
    } else if (typeof data.attributes !== "object") {
      pushError(invalidError(pointer))
    } else {

      // $.data.attributes.routingPlanId
      pointer = "/data/attributes/routingPlanId"
      if (typeof data.attributes.routingPlanId === "undefined") {
        pushError(missingError(pointer))
      } else if (data.attributes.routingPlanId === null) {
        pushError(nullError(pointer))
      } else if (typeof data.attributes.routingPlanId !== "string" || !uuidRegex.test(data.attributes.routingPlanId)) {
        pushError(invalidError(pointer))
      }

      // $.data.attributes.messageBatchReference
      pointer = "/data/attributes/messageBatchReference"
      if (typeof data.attributes.messageBatchReference === "undefined") {
        pushError(missingError(pointer))
      } else if (data.attributes.messageBatchReference === null) {
        pushError(nullError(pointer))
      } else if (typeof data.attributes.messageBatchReference !== "string" || !uuidRegex.test(data.attributes.messageBatchReference)) {
        pushError(invalidError(pointer))
      }

      // $.data.attributes.messages
      pointer = "/data/attributes/messages"
      if (typeof data.attributes.messages === "undefined") {
        pushError(missingError(pointer))
      } else if (data.attributes.messages === null) {
        pushError(nullError(pointer))
      } else if (!Array.isArray(data.attributes.messages)) {
        pushError(invalidError(pointer))
      } else if (data.attributes.messages.length === 0) {
        pushError(tooFewItemsError(pointer))
      } else {

        // $.data.attributes.recipients.x
        data.attributes.messages.forEach((message, index) => {
          pointer = "/data/attributes/messages/" + index
          if (typeof message === "undefined") {
            pushError(missingError(pointer))
          } else if (message === null) {
            pushError(nullError(pointer))
          } else if (typeof message !== "object") {
            pushError(invalidError(pointer))
          } else {

            // $.data.attributes.messages.x.messageReference
            pointer = "/data/attributes/messages/" + index + "/messageReference"
            if (typeof message.messageReference === "undefined") {
              pushError(missingError(pointer))
            } else if (message.messageReference === null) {
              pushError(nullError(pointer))
            } else if (typeof message.messageReference !== "string" || !uuidRegex.test(message.messageReference)) {
              pushError(invalidError(pointer))
            } else if (seenMessages.indexOf(message.messageReference) !== -1) {
              pushError(duplicateError(pointer))
            }
            seenMessages.push(message.messageReference)
          }

          // $.data.attributes.messages.x.recipient
          pointer = "/data/attributes/messages/" + index + "/recipient"
          if (typeof message.recipient === "undefined") {
            pushError(missingError(pointer))
          } else if (typeof message.recipient !== 'object') {
            pushError(invalidError(pointer))
          } else if (message.recipient === null) {
            pushError(nullError(pointer))
          } else {

            // $.data.attributes.messages.x.recipient.nhsNumber
            pointer = "/data/attributes/messages/" + index + "/recipient/nhsNumber"
            if (typeof message.recipient.nhsNumber === "undefined") {
              pushError(missingError(pointer))
            } else if (message.recipient.nhsNumber === null) {
              pushError(nullError(pointer))
            } else if (typeof message.recipient.nhsNumber !== "string" || !nhsNumberRegex.test(message.recipient.nhsNumber)) {
              pushError(invalidError(pointer))
            }

            // $.data.attributes.recipients.x.dateOfBirth
            pointer = "/data/attributes/messages/" + index + "/recipient/dateOfBirth"
            if (message.recipient.dateOfBirth && typeof message.recipient.dateOfBirth !== "string" || !dobRegex.test(message.recipient.dateOfBirth)) {
              pushError(invalidError(pointer))
            }

            // $.data.attributes.messages.x.personalisation
            pointer = "/data/attributes/messages/" + index + "/personalisation"
            if (typeof message.personalisation !== "object") {
              pushError(invalidError(pointer))
            }
          }

        })
      }
    }
  }
}


function pushError(error) {
  // Limit the amount of errors returned to 100 entries
  if (errors.length <= 100) {
    errors.push(error)
  }
}


function createErrorObject(code, title, detail, pointer) {
  return {
    "id": code,
    "links": {
      "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
    },
    "status": "400",
    "title": title,
    "detail": detail,
    "source": {
      "pointer": pointer
    }
  }
}

function missingError(pointer) {
  return createErrorObject(
    "CM_MISSING_VALUE",
    "Missing property",
    "The property at the specified location is required, but was not present in the request.",
    pointer
  )
}

function nullError(pointer) {
  return createErrorObject(
    "CM_NULL_VALUE",
    "Property cannot be null",
    "The property at the specified location is required, but a null value was passed in the request.",
    pointer
  )
}

function invalidError(pointer) {
  return createErrorObject(
    "CM_INVALID_VALUE",
    "Invalid value",
    "The property at the specified location does not allow this value.",
    pointer
  )
}

function duplicateError(pointer) {
  return createErrorObject(
    "CM_DUPLICATE_VALUE",
    "Duplicate value",
    "The property at the specified location is a duplicate, duplicated values are not allowed.",
    pointer
  )
}

function tooFewItemsError(pointer) {
  return createErrorObject(
    "CM_TOO_FEW_ITEMS",
    "Too few items",
    "The property at the specified location contains too few items.",
    pointer
  )
}

if (errors.length > 0) {
  context.setVariable("errors", JSON.stringify(errors))
} else {
  context.setVariable("errors", null)
}
