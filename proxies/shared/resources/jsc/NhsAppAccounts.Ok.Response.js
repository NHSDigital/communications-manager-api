const content = context.getVariable("response.content")

const virtualhosts = context.getVariable("virtualhost.aliases");
const hostname = virtualhosts.slice(-1)[0];
const internalHostname = context.getVariable("request.header.host");

const reqUrl = context.getVariable('proxy.url');
const baseUrl = reqUrl.split("?")[0].replace(internalHostname, hostname);

const parsedContent = JSON.parse(content)
let odsOrganisationCode = null;

if (parsedContent) {
  odsOrganisationCode = parsedContent.data.id

    if (parsedContent.links) {
      if (parsedContent.links.self) {
        parsedContent.links.self = replacePathRoot(baseUrl, parsedContent.links.self);
      }

      if (parsedContent.links.next) {
        parsedContent.links.next = replacePathRoot(baseUrl, parsedContent.links.next);
      }

      if (parsedContent.links.last) {
        parsedContent.links.last = replacePathRoot(baseUrl, parsedContent.links.last);
      }
    }
}

context.setVariable("odsOrganisationCode", odsOrganisationCode);
context.setVariable("response.content", JSON.stringify(parsedContent));
