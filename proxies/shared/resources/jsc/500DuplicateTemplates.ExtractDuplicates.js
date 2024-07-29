const body = context.getVariable("response.content");
const {message} = JSON.parse(body);
context.setVariable("data.duplicates", message.replace("Duplicate templates in routing config: ", "").replace(/\\/g, ""));