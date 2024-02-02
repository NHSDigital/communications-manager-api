const content = context.getVariable("request.content")
const data = JSON.parse(content).data
var messageBatchReference = null;

if (data && data.attributes) {
    messageReference = data.attributes.messageReference;
}

context.setVariable("data.payload", content);
context.setVariable("data.messageBatchReference", messageBatchReference);
