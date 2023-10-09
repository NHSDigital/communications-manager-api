const content = context.getVariable("response.content")

const reqUrl = context.getVariable('proxy.url');
const baseUrl = reqUrl.split("?")[0]

const data = JSON.parse(content).data
var messageId = null;

if (data) {
    messageId = data.id;
    data.links.self = data.links.self.replace("%PATH_ROOT%", baseUrl);
}

context.setVariable("messageId", messageId);
context.setVariable("response.content", JSON.stringify({ data: data }));
