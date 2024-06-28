const incomingCorrelationId = context.getVariable("request.header.x-correlation-id");
const apigeeMessageId = context.getVariable("messageid");

if (incomingCorrelationId) {
    context.setVariable("backendCorrelationId", incomingCorrelationId);
}
else {
    context.setVariable("backendCorrelationId", apigeeMessageId);
}
