/**
 * This script validates the data in the body of a POST request to the /v1/messages endpoint, returning an
 * array of up to 100 error responses to be returned by Apigee as a 400 error response.
 *
 * It is called by the JavaScript.Messages.Create.Validate policy.
 */


var content = context.getVariable("request.content")
var errors = []

var all
var parseFailed = false;
try {
    all = JSON.parse(content)
} catch (e) {
    errors.push(invalidError("/"))
    parseFailed = true;
}

function validateRecipient(errors, recipient) {
    const validRecipientObject = validateObject(errors, recipient, "/data/attributes/recipient");
    if (validRecipientObject) {
        validateNhsNumber(errors, recipient.nhsNumber, "/data/attributes/recipient/nhsNumber");
    }
}

function validateOriginator(errors, originator) {
    const validOriginatorObject = validateObject(errors, originator, "/data/attributes/originator");
    if (validOriginatorObject) {
        validateOdsCode(errors, originator.odsCode, "/data/attributes/originator/odsCode");
    }
}

function validateAttributes(errors, attributes) {
    const validAttributesObject = validateObject(errors, attributes, "/data/attributes");
    if (validAttributesObject) {
        validateUuid(errors, attributes.routingPlanId, "/data/attributes/routingPlanId");
        validateString(errors, attributes.messageReference, "/data/attributes/messageReference");

        validateRecipient(errors, attributes.recipient);

        if (!isUndefined(attributes.originator)) {
            validateOriginator(errors, attributes.originator);
        }

        if (!isUndefined(attributes.personalisation)) {
            validateObject(errors, attributes.personalisation, "/data/attributes/personalisation");
        }
    }
}

function validateData(errors, data) {
    const validDataObject = validateObject(errors, data, "/data");
    if (validDataObject) {
        validateConstantString(errors, data.type, "/data/type", "Message");
        validateAttributes(errors, data.attributes);
    }
}

const validate = () => {
    if (parseFailed) return;
    if (all) {
        var data = all.data;
        validateData(errors, data);
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
