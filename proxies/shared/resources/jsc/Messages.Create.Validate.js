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

                // $.data.attributes.recipient
                const validRecipientObject = validateObject(errors, data.attributes.recipient, "/data/attributes/recipient")
                if (validRecipientObject) {

                    // $.data.attributes.recipient.nhsNumber
                    validateNhsNumber(errors, data.attributes.recipient.nhsNumber, "/data/attributes/recipient/nhsNumber")
                }

                if (!isUndefined(data.attributes.originator)) {
                  // $.data.attributes.originator
                  const validOriginatorObject = validateObject(errors, data.attributes.originator, "/data/attributes/originator")
                  if (validOriginatorObject) {
                    // $.data.attributes.originator.odsCode
                    validateOdsCode(errors, data.attributes.originator.odsCode, "/data/attributes/originator/odsCode")
                  }
                }

                // $.data.attributes.personalisation
                if (!isUndefined(data.attributes.personalisation)) {
                  validateObject(errors, data.attributes.personalisation, "/data/attributes/personalisation")
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
