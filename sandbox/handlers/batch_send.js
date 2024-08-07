import KSUID from "ksuid"
import {
  sendError,
  writeLog,
  hasValidGlobalTemplatePersonalisation,
} from "./utils.js"
import {
  validSendingGroupIds,
  invalidRoutingPlanId,
  sendingGroupIdWithMissingNHSTemplates,
  sendingGroupIdWithMissingTemplates,
  sendingGroupIdWithDuplicateTemplates,
  duplicateTemplates,
  trigger500SendingGroupId,
  trigger425SendingGroupId,
  globalFreeTextNhsAppSendingGroupId,
  noDefaultOdsClientAuth,
  noOdsChangeClientAuth,
} from "./config.js"

export async function batchSend(req, res, next) {
  const { headers, body } = req;
  if (headers.authorization === "banned") {
    sendError(
      res,
      403,
      "Request rejected because client service ban is in effect"
    );
    next();
    return;
  }

  if (!body) {
    sendError(res, 400, "Missing request body");
    next();
    return;
  }

  const { data } = body;
  if (!data) {
    sendError(res, 400, "Missing request body data");
    next();
    return;
  }

  const { type, attributes } = data;
  if (!type) {
    sendError(res, 400, "Missing request body data type");
    next();
    return;
  }

  if (type !== "MessageBatch") {
    sendError(res, 400, "Request body data type is not MessageBatch");
    next();
    return;
  }

  if (!attributes) {
    sendError(res, 400, "Missing request body data attributes");
    next();
    return;
  }

  const { routingPlanId, messages } = attributes;
  if (!routingPlanId) {
    sendError(res, 400, "Missing routingPlanId");
    next();
    return;
  }

  if (!attributes.messageBatchReference) {
    sendError(res, 400, "Missing messageBatchReference");
    next();
    return;
  }

  if (!Array.isArray(messages)) {
    sendError(res, 400, "Missing messages array");
    next();
    return;
  }

  // Note: the docker container uses node:12 which does not support optional chaining
  const odsCodes = messages.map((message) => message && message.originator ? message.originator.odsCode : undefined
  );
  if (odsCodes.includes(undefined) && req.headers.authorization === noDefaultOdsClientAuth) {
    sendError(
      res,
      400,
      'odsCode must be provided'
    )
    next();
    return;
  }

  if (odsCodes.filter((o) => o !== undefined).length > 0 && req.headers.authorization === noOdsChangeClientAuth) {
    sendError(
      res,
      400,
      'odsCode was provided but ODS code override is not enabled for the client'
    )
    next();
    return;
  }

  const messageReferences = messages.map((message) => message.messageReference);
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

  if (!validSendingGroupIds[routingPlanId]) {
    sendError(
      res,
      404,
      `Routing Config does not exist for clientId "sandbox_client_id" and routingPlanId "${routingPlanId}"`
    );
    next();
    return;
  }

  if (routingPlanId === invalidRoutingPlanId) {
    sendError(res, 400, "Invalid Routing Config");
    next();
    return;
  }

  if (routingPlanId === trigger425SendingGroupId) {
    sendError(
      res,
      425,
      "Message with this idempotency key is already being processed"
    );
    next();
    return;
  }

  if (
    routingPlanId === globalFreeTextNhsAppSendingGroupId &&
    messages.findIndex(
      (message) =>
        !hasValidGlobalTemplatePersonalisation(message.personalisation)
    ) > -1
  ) {
    sendError(res, 400, "Expect single personalisation field of 'body'");
    next();
    return;
  }

  if (routingPlanId === sendingGroupIdWithMissingNHSTemplates) {
    sendError(
      res,
      500,
      `NHS App Template does not exist with internalTemplateId: invalid-template`
    );
    next();
    return;
  }

  if (routingPlanId === sendingGroupIdWithMissingTemplates) {
    sendError(
      res,
      500,
      `Templates required in "${routingPlanId}" routing config not found`
    );
    next();
    return;
  }

  if (routingPlanId === sendingGroupIdWithDuplicateTemplates) {
    sendError(
      res,
      500,
      `Duplicate templates in routing config: ${JSON.stringify(
        duplicateTemplates
      )}`
    );
    next();
    return;
  }

  if (routingPlanId === trigger500SendingGroupId) {
    sendError(res, 500, "Error writing request items to DynamoDB");
    next();
    return;
  }

  writeLog(res, "warn", {
    message: "/api/v1/send",
    req: {
      path: req.path,
      query: req.query,
      headers: req.rawHeaders,
      payload: body,
    },
  });

  res.json({
    requestId: KSUID.randomSync(new Date()).string,
    routingPlan: {
      id: routingPlanId,
      version: "1",
    },
  });
  res.end();
  next();
}
