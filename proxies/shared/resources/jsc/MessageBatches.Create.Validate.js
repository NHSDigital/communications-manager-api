/**
 * This script validates the data in the body of a POST request to the /v1/message-batches endpoint, returning an
 * array of up to 100 error responses to be returned by Apigee as a 400 error response.
 *
 * It is called by the JavaScript.MessageBatches.Create.Validate policy.
 */

var content = context.getVariable("request.content");
var errors = [];

var all;
var parseFailed = false;
try {
  all = JSON.parse(content);
} catch (e) {
  errors.push(invalidError("/"));
  parseFailed = true;
}

function validateBatchMessage(errors, message, index, seenMessages) {
  var pointer = "/data/attributes/messages/" + index;

  // Limit the amount of errors returned to 100 entries
  if (errors.length >= 100) {
    return null;
  }

  if (!validateObject(errors, message, pointer)) return;

  pointer = "/data/attributes/messages/" + index + "/messageReference";
  const validMessageReference = validateString(
    errors,
    message.messageReference,
    pointer
  );
  if (validMessageReference) {
    if (seenMessages[message.messageReference]) {
      errors.push(duplicateError(pointer));
    } else {
      seenMessages[message.messageReference] = 1;
    }
  }

  const validRecipientObject = validateObject(
    errors,
    message.recipient,
    "/data/attributes/messages/" + index + "/recipient"
  );
  if (validRecipientObject) {
    validateNhsNumber(
      errors,
      message.recipient.nhsNumber,
      "/data/attributes/messages/" + index + "/recipient/nhsNumber"
    );
  }

  if (!isUndefined(message.originator)) {
    const validOriginatorObject = validateObject(
      errors,
      message.originator,
      "/data/attributes/messages/" + index + "/originator"
    );
    if (validOriginatorObject) {
      validateOdsCode(
        errors,
        message.originator.odsCode,
        "/data/attributes/messages/" + index + "/originator/odsCode"
      );
    }
  }

  pointer = "/data/attributes/messages/" + index + "/personalisation";
  if (!isUndefined(message.personalisation)) {
    validateObject(errors, message.personalisation, pointer);
  }
}

function validateBatchAttributes(errors, attributes, seenMessages) {
  const validAttributesObject = validateObject(
    errors,
    attributes,
    "/data/attributes"
  );
  if (validAttributesObject) {
    validateUuid(
      errors,
      attributes.routingPlanId,
      "/data/attributes/routingPlanId"
    );
    validateString(
      errors,
      attributes.messageBatchReference,
      "/data/attributes/messageBatchReference"
    );

    const validArray = validateArray(
      errors,
      attributes.messages,
      "/data/attributes/messages",
      1
    );
    if (validArray) {
      if (attributes.messages.length > 45000) {
        errors.push(tooManyItemsError("/data/attributes/messages"));
        return null;
      }
      attributes.messages.forEach((message, index) => {
        validateBatchMessage(errors, message, index, seenMessages);
      });
    }
  }
}

function validateBatchData(errors, data, seenMessages) {
  const validDataObject = validateObject(errors, data, "/data");
  if (validDataObject) {
    validateConstantString(errors, data.type, "/data/type", "MessageBatch");
    validateBatchAttributes(errors, data.attributes, seenMessages);
  }
}

const validate = () => {
  if (parseFailed) return;
  if (all) {
    var seenMessages = {};
    var data = all.data;
    validateBatchData(errors, data, seenMessages);
  }
  errors = errors.slice(0, 100);
};

validate();

if (errors.length > 0) {
  context.setVariable("generic_status_code", errors[0].status);
  context.setVariable("errors", JSON.stringify(errors));
} else {
  context.setVariable("generic_status_code", null);
  context.setVariable("errors", null);
}
