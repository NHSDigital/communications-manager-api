const acceptHeader = context.getVariable("request.header.accept");

var responseType = "application/vnd.api+json";

if (acceptHeader === "application/json") {
    responseType = "application/json";
}

context.setVariable("response.header.content-type", responseType);
context.setVariable("error.header.content-type", responseType);