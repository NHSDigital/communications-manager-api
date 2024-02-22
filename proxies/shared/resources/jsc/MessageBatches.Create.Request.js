const content = context.getVariable("request.content")
const data = JSON.parse(content).data
var messages = null;
var routingPlanId = null;
var messageBatchReference = null;

if (data && data.attributes) {
    routingPlanId = data.attributes.routingPlanId;
    messageBatchReference = data.attributes.messageBatchReference;

    if (data.attributes.messages) {
        messages = [];
        data.attributes.messages.forEach((message) => {
            if (message) {
                messages.push({
                    nhsNumber           : message.recipient ? message.recipient.nhsNumber : null,
                    dateOfBirth         : message.recipient ? message.recipient.dateOfBirth : null,
                    requestItemRefId    : message.messageReference,
                    personalisation     : message.personalisation
                });
            }
        });
    }
}

context.setVariable("data.payload", JSON.stringify({
    "sendingGroupId" : routingPlanId,
    "requestRefId" : messageBatchReference,
    "data" : messages
}));
context.setVariable("data.messageBatchReference", messageBatchReference);
