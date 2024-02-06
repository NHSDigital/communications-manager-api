/* istanbul ignore file */
const KSUID = require("ksuid");
const { sendError, write_log } = require('./utils')
const {
    validSendingGroupIds,
    invalidRoutingPlanId,
    sendingGroupIdWithMissingNHSTemplates,
    sendingGroupIdWithMissingTemplates,
    sendingGroupIdWithDuplicateTemplates,
    duplicateTemplates,
    trigger500SendingGroupId,
    trigger425SendingGroupId,
} = require('./config')

async function batch_send(req, res, next) {
    if (req.headers["authorization"] === "banned") {
        sendError(res, 403, "Request rejected because client service ban is in effect");
        next();
        return;
    }

    if (!req.body) {
        sendError(res, 400, "Missing request body");
        next();
        return;
    }

    if (!req.body.data) {
        sendError(res, 400, "Missing request body data");
        next();
        return;
    }

    if (req.body.data.type !== "MessageBatch") {
        sendError(req, 400, "Request body data type is not MessageBatch");
        next();
        return;
    }

    if (!req.body.data.attributes) {
        sendError(res, 400, "Missing request body data attributes");
        next();
        return;
    }

    if (!req.body.attributes.routingPlanId) {
        sendError(res, 400, "Missing routingPlanId");
        next();
        return;
    }

    if (!req.body.attributes.messageBatchReference) {
        sendError(res, 400, "Missing messageBatchReference");
        next();
        return;
    }

    if (!Array.isArray(req.body.data.attributes.messages)) {
        sendError(res, 400, "Missing data array");
        next();
        return;
    }

    const messageReferences = req.body.data.attributes.messages.map(
        (message) => message.messageReference
    );

    if (messageReferences.includes(undefined)) {
        sendError(res, 400, "Missing messageReferences");
        next();
        return;
    }

    if (new Set(messageReferences).size !== messageReferences.length) {
        sendError(res, 400, "Duplicate messageReferences");
        next();
        return;
    }

    if (!validSendingGroupIds[req.body.data.attributes.routingPlanId]) {
        sendError(res, 404, `Routing Config does not exist for clientId "sandbox_client_id" and routingPlanId "${req.body.data.attributes.routingPlanId}"`);
        next();
        return;
    }

    if (req.body.data.attributes.routingPlanId === invalidRoutingPlanId) {
        sendError(res, 400, "Invalid Routing Config");
        next();
        return;
    }

    if (req.body.data.attributes.routingPlanId === trigger425SendingGroupId) {
        sendError(res, 425, "Message with this idempotency key is already being processed");
        next();
        return;
    }

    if (req.body.data.attributes.routingPlanId === sendingGroupIdWithMissingNHSTemplates) {
        sendError(res, 500, `NHS App Template does not exist with internalTemplateId: invalid-template`);
        next();
        return;
    }

    if (req.body.data.attributes.routingPlanId === sendingGroupIdWithMissingTemplates) {
        sendError(res, 500, `Templates required in "${req.body.data.attributes.routingPlanId}" routing config not found`);
        next();
        return;
    }

    if (req.body.data.attributes.routingPlanId === sendingGroupIdWithDuplicateTemplates) {
        sendError(res, 500, `Duplicate templates in routing config: ${JSON.stringify(duplicateTemplates)}`);
        next();
        return;
    }

    if (req.body.data.attributes.routingPlanId === trigger500SendingGroupId) {
        sendError(res, 500, "Error writing request items to DynamoDB");
        next();
        return;
    }

    write_log(res, "warn", {
        message: "/api/v1/send",
        req: {
            path: req.path,
            query: req.query,
            headers: req.rawHeaders,
            payload: req.body
        }
    });

    res.json({
        requestId: KSUID.randomSync(new Date()).string,
        routingPlan: {
            id: req.body.data.attributes.routingPlanId,
            version: "1"
        }
    });
    res.end();
    next();
}

module.exports = {
    batch_send
}
