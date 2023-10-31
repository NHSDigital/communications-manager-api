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

// format errors object
try {
  const content = context.getVariable("error.content")
  const errors = JSON.parse(content).errors

  if (errors) {
    context.setVariable("error.content", JSON.stringify({ errors: errors }));
  }
} catch (e) {
  //
}
