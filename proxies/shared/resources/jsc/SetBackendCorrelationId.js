const incomingCorrelationId = context.getVariable("request.header.x-correlation-id");
const messageId = context.getVariable("messageid");

if (incomingCorrelationId && messageId) {
    context.setVariable("backendCorrelationId", incomingCorrelationId);
}
else {
    context.setVariable("backendCorrelationId", messageId);
}
