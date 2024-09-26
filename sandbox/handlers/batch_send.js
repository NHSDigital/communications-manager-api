import KSUID from "ksuid";
import { sendError, writeLog } from "./utils.js";
import { getGlobalFreeTextError } from "./error_scenarios/global_free_text.js";
import { getSendingGroupIdError } from "./error_scenarios/sending_group_id.js";
import { getOdsCodeError } from "./error_scenarios/ods_code.js";
import { mandatoryBatchMessageFieldValidation } from "./validation/mandatory_batch_message_fields.js";
import { getAlternateContactDetailsError } from "./error_scenarios/override_contact_details.js";

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

  const mandatoryFieldError = mandatoryBatchMessageFieldValidation(body);
  if (mandatoryFieldError !== null) {
    const [errorCode, errorMessage] = mandatoryFieldError;
    sendError(res, errorCode, errorMessage);
    next();
    return;
  }

  const { routingPlanId, messages } = body.data.attributes;

  const messagePersonsalisations = messages.map(
    (message) => message.personalisation
  );
  for (const personalisation of messagePersonsalisations) {
    const globalFreeTextError = getGlobalFreeTextError(
      personalisation,
      routingPlanId
    );

    if (globalFreeTextError !== null) {
      const [errorCode, errorMessage] = globalFreeTextError;
      sendError(res, errorCode, errorMessage);
      next();
      return;
    }
  }

  const odsCodes = messages.map(
    (message) => message && message.originator?.odsCode
  );
  for (const odsCode of odsCodes) {
    const odsCodeError = getOdsCodeError(odsCode, req.headers.authorization);

    if (odsCodeError !== null) {
      const [errorCode, errorMessage] = odsCodeError;
      sendError(res, errorCode, errorMessage);
      next();
      return;
    }
  }

  const sendingGroupIdError = getSendingGroupIdError(routingPlanId);
  if (sendingGroupIdError !== null) {
    const [errorCode, errorMessage] = sendingGroupIdError;
    sendError(res, errorCode, errorMessage);
    next();
    return;
  }

  const alternateContactDetails = messages.map(
    (message) => message.recipient?.contactDetails
  );
  for (const contactDetail of alternateContactDetails) {
    const alternateContactDetailsError = getAlternateContactDetailsError(
      contactDetail,
      req.headers.authorization,
      "/data/attributes/messages"
    );
    if (alternateContactDetailsError !== null) {
      const [errorCode, errorMessage, errors] = alternateContactDetailsError;
      sendError(res, errorCode, errorMessage, errors);
      next();
      return;
    }
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
