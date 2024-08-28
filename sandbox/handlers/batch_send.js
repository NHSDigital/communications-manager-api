import KSUID from "ksuid"
import {
  sendError,
  writeLog,
  hasValidGlobalTemplatePersonalisation,
} from "./utils.js"
import {
  globalFreeTextNhsAppSendingGroupId,
} from "./config.js"
import { getSendingGroupIdError } from "./error_scenarios/sending_group_id.js"
import { getOdsCodeError } from "./error_scenarios/ods_code.js"

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

  const odsCodes = messages.map((message) => message && message.originator?.odsCode)
  for (const odsCode of odsCodes) {
    const odsCodeError = getOdsCodeError(odsCode, req.headers.authorization)

    if (odsCodeError !== null) {
      const [errorCode, errorMessage] = odsCodeError
      sendError(res, errorCode, errorMessage)
      next()
      return;
    }
  }

  const sendingGroupIdError = getSendingGroupIdError(routingPlanId)
  if (sendingGroupIdError !== null) {
    const [errorCode, errorMessage] = sendingGroupIdError
    sendError(
      res,
      errorCode,
      errorMessage
    )
    next()
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
