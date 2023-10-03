const content = context.getVariable("response.content")
const data = JSON.parse(content).data
var messageId = null;

if (data) {
    messageId = data.id;
}

context.setVariable("messageId", messageId);
