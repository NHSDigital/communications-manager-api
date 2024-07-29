const content = context.getVariable("request.content")
const {data} = JSON.parse(content)
let messageBatchReference = null;

if (data && data.attributes) {
    messageBatchReference = data.attributes.messageBatchReference;
}

context.setVariable("data.payload", content);
context.setVariable("data.messageBatchReference", messageBatchReference);
