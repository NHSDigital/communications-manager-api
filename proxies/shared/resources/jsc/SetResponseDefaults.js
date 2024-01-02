const acceptHeader = context.getVariable("request.header.accept");

var responseType = "application/vnd.api+json";

if (acceptHeader === "application/json") {
    responseType = "application/json";
}

// set the content type
context.setVariable("response.header.content-type", responseType);
context.setVariable("error.header.content-type", responseType);

// set our cache control header
context.setVariable("response.header.Cache-Control", "no-cache, no-store, must-revalidate");
context.setVariable("error.header.Cache-Control", "no-cache, no-store, must-revalidate");

// set our x-content-type-options-header
context.setVariable("response.header.X-Content-Type-Options", "nosniff");
context.setVariable("error.header.X-Content-Type-Options", "nosniff");

// remove aws headers
const headers = context.getVariable("response.header");
const headerRegex = /^x-amz-/;
Object.keys(headers).forEach(function (headerKey) {
  if (headerRegex.test(headerKey.toLowerCase())) {
    context.removeVariable("response.header." + headerKey);
  }
});

// format errors and response objects
try {
  const errorContent = context.getVariable("error.content")
  const responseContent = context.getVariable("response.content")

  if (errorContent) context.setVariable("error.content", JSON.stringify(JSON.parse(errorContent)))
  if (responseContent) context.setVariable("response.content", JSON.stringify(JSON.parse(responseContent)))

} catch (e) {
  //
}
