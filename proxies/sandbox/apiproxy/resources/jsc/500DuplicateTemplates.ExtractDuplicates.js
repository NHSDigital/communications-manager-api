const body = context.getVariable("response.content");
const message = JSON.parse(body).message;
context.setVariable("data.duplicates", message.replace("Duplicate templates found: ", "").replace(/\\/g, ""));