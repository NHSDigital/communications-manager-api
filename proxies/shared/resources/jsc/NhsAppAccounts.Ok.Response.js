const content = context.getVariable("response.content")

const virtualhosts = context.getVariable("virtualhost.aliases");
const hostname = virtualhosts.slice(-1)[0];
const internalHostname = context.getVariable("request.header.host");

const reqUrl = context.getVariable('proxy.url');
const baseUrl = reqUrl.split("?")[0].replace(internalHostname, hostname);

const parsedContent = JSON.parse(content)
var odsOrganisationCode = null;

const replacePathRoot = (link) => {
  const withoutPathRoot = link.self.replace("%PATH_ROOT%", "").split("").reverse().join("");
  if (baseUrl.split("").reverse().join("").indexOf(withoutPathRoot) === 0) {
    return baseUrl;
  } else {
    return link.replace("%PATH_ROOT%", baseUrl);
  }
};

if (parsedContent) {
  odsOrganisationCode = parsedContent.data.id

    if (parsedContent.links) {
      if (parsedContent.links.self) {
        parsedContent.links.self = replacePathRoot(parsedContent.links.self);
      }

      if (parsedContent.links.next) {
        parsedContent.links.next = replacePathRoot(parsedContent.links.next);
      }

      if (parsedContent.links.last) {
        parsedContent.links.last = replacePathRoot(parsedContent.links.last);
      }
    }
}

context.setVariable("odsOrganisationCode", odsOrganisationCode);
context.setVariable("response.content", JSON.stringify(parsedContent));
