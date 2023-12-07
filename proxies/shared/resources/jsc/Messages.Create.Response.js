const content = context.getVariable("response.content")

const virtualhosts = context.getVariable("virtualhost.aliases");
const hostname = virtualhosts.slice(-1)[0];
const internalHostname = context.getVariable("request.header.host");

const reqUrl = context.getVariable('proxy.url');
const baseUrl = reqUrl.split("?")[0].replace(internalHostname, hostname);

const data = JSON.parse(content).data
var messageId = null;

if (data) {
    messageId = data.id;

    // temporary change to remove all links from responses using this script
    // this is due to the send single going live before the get single
    if (data.links) {
        delete data.links;
    }

    if (data.links && data.links.self) {
        data.links.self = data.links.self.replace("%PATH_ROOT%", baseUrl);
    }
}

context.setVariable("messageId", messageId);
context.setVariable("response.content", JSON.stringify({ data: data }));