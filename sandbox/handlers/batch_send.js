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
import { mandatoryBatchMessageFieldValidation } from "./validation/mandatory_batch_message_fields.js"

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

  const mandatoryFieldError = mandatoryBatchMessageFieldValidation(body)
  if (mandatoryFieldError !== null) {
    const [errorCode, errorMessage] = mandatoryFieldError
    sendError(res, errorCode, errorMessage)
    next()
    return;
  } 

  const { routingPlanId, messages } = body.data.attributes

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
