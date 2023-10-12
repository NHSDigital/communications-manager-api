/**
 * This script validates the data in the body of a POST request to the /v1/messages endpoint, returning an
 * array of up to 100 error responses to be returned by Apigee as a 400 error response.
 *
 * It is called by the JavaScript.Messages.Create.Validate policy.
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
        var data = all.data;

        // $.data
        const validDataObject = validateObject(errors, data, "/data")
        if (validDataObject) {

            // $.data.type
            validateConstantString(errors, data.type, "/data/type", "Message")

            // $.data.attributes
            const validAttributesObject = validateObject(errors, data.attributes, "/data/attributes")
            if (validAttributesObject) {

                // $.data.attributes.routingPlanId
                validateUuid(errors, data.attributes.routingPlanId, "/data/attributes/routingPlanId")

                // $.data.attributes.messageReference
                validateUuid(errors, data.attributes.messageReference, "/data/attributes/messageReference")

                // $.data.attributes.recipient
                const validRecipientObject = validateObject(errors, data.attributes.recipient, "/data/attributes/recipient")
                if (validRecipientObject) {

                    // $.data.attributes.recipient.nhsNumber
                    validateNhsNumber(errors, data.attributes.recipient.nhsNumber, "/data/attributes/recipient/nhsNumber")

                    // $.data.attributes.recipients.dateOfBirth
                    validateDob(errors, data.attributes.recipient.dateOfBirth, "/data/attributes/recipient/dateOfBirth")

                }

                // $.data.attributes.personalisation
                pointer = "/data/attributes/personalisation";
                if (!isUndefined(data.attributes.personalisation) && typeof data.attributes.personalisation !== "object") {
                    errors.push(invalidError(pointer));
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
