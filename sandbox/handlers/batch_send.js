import KSUID from "ksuid"
import {
  sendError,
  write_log,
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
} from "./config.js"

export async function batch_send(req, res, next) {
  sendError(res, 400, "TEST ERROR");
  next();
  return;
  // const { headers, body } = req;
  // if (headers["authorization"] === "banned") {
  //   sendError(
  //     res,
  //     403,
  //     "Request rejected because client service ban is in effect"
  //   );
  //   next();
  //   return;
  // }

  // if (!body) {
  //   sendError(res, 400, "Missing request body");
  //   next();
  //   return;
  // }

  // const data = body.data;
  // if (!data) {
  //   sendError(res, 400, "Missing request body data");
  //   next();
  //   return;
  // }

  // const type = data.type;
  // if (!type) {
  //   sendError(res, 400, "Missing request body data type");
  //   next();
  //   return;
  // }

  // if (type !== "MessageBatch") {
  //   sendError(res, 400, "Request body data type is not MessageBatch");
  //   next();
  //   return;
  // }

  // const attributes = data.attributes;
  // if (!attributes) {
  //   sendError(res, 400, "Missing request body data attributes");
  //   next();
  //   return;
  // }

  // const routingPlanId = attributes.routingPlanId;
  // if (!routingPlanId) {
  //   sendError(res, 400, "Missing routingPlanId");
  //   next();
  //   return;
  // }

  // if (!attributes.messageBatchReference) {
  //   sendError(res, 400, "Missing messageBatchReference");
  //   next();
  //   return;
  // }

  // const messages = attributes.messages;
  // if (!Array.isArray(messages)) {
  //   sendError(res, 400, "Missing messages array");
  //   next();
  //   return;
  // }

  // const messageReferences = messages.map((message) => message.messageReference);
  // if (messageReferences.includes(undefined)) {
  //   sendError(res, 400, "Missing messageReferences");
  //   next();
  //   return;
  // }

  // if (new Set(messageReferences).size !== messageReferences.length) {
  //   sendError(res, 400, "Duplicate messageReferences");
  //   next();
  //   return;
  // }

  // if (!validSendingGroupIds[routingPlanId]) {
  //   sendError(
  //     res,
  //     404,
  //     `Routing Config does not exist for clientId "sandbox_client_id" and routingPlanId "${routingPlanId}"`
  //   );
  //   next();
  //   return;
  // }

  // if (routingPlanId === invalidRoutingPlanId) {
  //   sendError(res, 400, "Invalid Routing Config");
  //   next();
  //   return;
  // }

  // if (routingPlanId === trigger425SendingGroupId) {
  //   sendError(
  //     res,
  //     425,
  //     "Message with this idempotency key is already being processed"
  //   );
  //   next();
  //   return;
  // }

  // if (
  //   routingPlanId === globalFreeTextNhsAppSendingGroupId &&
  //   messages.findIndex(
  //     (message) =>
  //       !hasValidGlobalTemplatePersonalisation(message.personalisation)
  //   ) > -1
  // ) {
  //   sendError(res, 400, "Expect single personalisation field of 'body'");
  //   next();
  //   return;
  // }

  // if (routingPlanId === sendingGroupIdWithMissingNHSTemplates) {
  //   sendError(
  //     res,
  //     500,
  //     `NHS App Template does not exist with internalTemplateId: invalid-template`
  //   );
  //   next();
  //   return;
  // }

  // if (routingPlanId === sendingGroupIdWithMissingTemplates) {
  //   sendError(
  //     res,
  //     500,
  //     `Templates required in "${routingPlanId}" routing config not found`
  //   );
  //   next();
  //   return;
  // }

  // if (routingPlanId === sendingGroupIdWithDuplicateTemplates) {
  //   sendError(
  //     res,
  //     500,
  //     `Duplicate templates in routing config: ${JSON.stringify(
  //       duplicateTemplates
  //     )}`
  //   );
  //   next();
  //   return;
  // }

  // if (routingPlanId === trigger500SendingGroupId) {
  //   sendError(res, 500, "Error writing request items to DynamoDB");
  //   next();
  //   return;
  // }

  // write_log(res, "warn", {
  //   message: "/api/v1/send",
  //   req: {
  //     path: req.path,
  //     query: req.query,
  //     headers: req.rawHeaders,
  //     payload: body,
  //   },
  // });

  // res.json({
  //   requestId: KSUID.randomSync(new Date()).string,
  //   routingPlan: {
  //     id: routingPlanId,
  //     version: "1",
  //   },
  // });
  // res.end();
  // next();
}