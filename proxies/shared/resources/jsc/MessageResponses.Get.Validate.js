/* global context, validateUuidMessageId */

const errors = []

validateUuidMessageId(errors, context.getVariable("data.messageId"), "messageId");

if (errors.length > 0) {
    context.setVariable("generic_status_code", errors[0].status);
    context.setVariable("errors", JSON.stringify(errors));
} else {
    context.setVariable("generic_status_code", null);
    context.setVariable("errors", null);
}
