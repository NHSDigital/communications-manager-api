const content = context.getVariable("response.content")

const virtualhosts = context.getVariable("virtualhost.aliases");
const hostname = virtualhosts.slice(-1)[0];
const internalHostname = context.getVariable("request.header.host");

const reqUrl = context.getVariable('proxy.url');
const baseUrl = reqUrl.split("?")[0].replace(internalHostname, hostname);

const correlationId = context.getVariable("response.header.x-correlation-id");

const data = JSON.parse(content).data
var messageId = null;

if (data) {
    messageId = data.id

    if (data.links && data.links.self) {
      data.links.self = replacePathRoot(baseUrl, data.links.self);
    }
}

context.setVariable("messageId", messageId);
context.setVariable("correlationId", correlationId);
context.setVariable("response.content", JSON.stringify({ data: data }));
