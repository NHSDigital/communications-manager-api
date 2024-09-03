import KSUID from "ksuid";
import { sendError, writeLog, hasValidGlobalTemplatePersonalisation } from "./utils.js";
import {
  validSendingGroupIds,
  globalFreeTextNhsAppSendingGroupId,
} from "./config.js"
import { getSendingGroupIdError } from "./error_scenarios/sending_group_id.js";
import { getOdsCodeError } from "./error_scenarios/ods_code.js";
import { mandatorySingleMessageFieldValidation } from "./validation/mandatory_single_message_fields.js";
import { getAlternateContactDetailsError } from "./error_scenarios/override_contact_details.js";

export async function messages(req, res, next) {
  if (req.headers.authorization === "banned") {
    sendError(
      res,
      403,
      "Request rejected because client service ban is in effect"
    );
    next();
    return;
  }

  const mandatoryFieldError = mandatorySingleMessageFieldValidation(req.body)
  if (mandatoryFieldError !== null) {
    const [errorCode, errorMessage] = mandatoryFieldError
    sendError(res, errorCode, errorMessage)
    next()
    return;
  }

  const { routingPlanId } = req.body.data.attributes;

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
    !hasValidGlobalTemplatePersonalisation(req.body.data.attributes.personalisation)
  ) {
    sendError(res, 400, "Expect single personalisation field of 'body'");
    next();
    return;
  }

  const odsCode = req.body.data?.attributes?.originator?.odsCode;
  const odsCodeError = getOdsCodeError(odsCode, req.headers.authorization)
  if (odsCodeError !== null) {
    const [odsCodeErrorCode, odsCodeErrorMessage] = odsCodeError
    sendError(res, odsCodeErrorCode, odsCodeErrorMessage)
    next()
    return;
  }

  const alternateContactDetails = req.body.data?.attributes?.recipient?.contactDetails
  const alternateContactDetailsError = getAlternateContactDetailsError(alternateContactDetails, req.headers.authorization, '/data/attributes')
  if (alternateContactDetailsError !== null) {
    const [errorCode, errorMessage, errors] = alternateContactDetailsError
    sendError(
      res,
      errorCode,
      errorMessage,
      errors
    )
    next()
    return;
  }

  writeLog(res, "warn", {
    message: "/api/v1/messages",
    req: {
      path: req.path,
      query: req.query,
      headers: req.rawHeaders,
      payload: req.body,
    },
  });

  const messageId = KSUID.randomSync(new Date()).string;

  res.status(201).json({
    data: {
      type: "Message",
      id: messageId,
      attributes: {
        routingPlan: {
          id: routingPlanId,
          version: validSendingGroupIds[routingPlanId],
        },
        messageReference: req.body.data.attributes.messageReference,
        messageStatus: "created",
        timestamps: {
          created: new Date(),
        },
      },
      links: {
        self: `%PATH_ROOT%/${messageId}`,
      },
    },
  });
  res.end();
  next();
}
