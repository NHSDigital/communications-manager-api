import KSUID from "ksuid";
import { sendError, writeLog, hasValidGlobalTemplatePersonalisation } from "./utils.js";
import {
  sendingGroupIdWithMissingNHSTemplates,
  sendingGroupIdWithMissingTemplates,
  sendingGroupIdWithDuplicateTemplates,
  duplicateTemplates,
  trigger500SendingGroupId,
  validSendingGroupIds,
  globalFreeTextNhsAppSendingGroupId,
  noDefaultOdsClientAuth,
  noOdsChangeClientAuth
} from "./config.js"

// Note: the docker container uses node:12 which does not support optional chaining
function getOriginatorOdsCode(req) {
  let odsCode;
  try {
    odsCode = req.body.data.attributes.originator.odsCode;
  } catch {
    odsCode = undefined;
  }
  return odsCode;
}

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

  if (!req.body) {
    sendError(res, 400, "Missing request body");
    next();
    return;
  }

  const { routingPlanId } = req.body.data.attributes;
  if (!validSendingGroupIds[routingPlanId]) {
    sendError(
      res,
      404,
      `Routing Config does not exist for clientId "sandbox_client_id" and routingPlanId "${req.body.data.attributes.routingPlanId}"`
    );
    next();
    return;
  }

  const odsCode = getOriginatorOdsCode(req);
  if (!odsCode && req.headers.authorization === noDefaultOdsClientAuth) {
    sendError(
      res,
      400,
      'odsCode must be provided'
    )
    next();
    return;
  }

  if (odsCode && req.headers.authorization === noOdsChangeClientAuth) {
    sendError(
      res,
      400,
      'odsCode was provided but ODS code override is not enabled for the client'
    )
    next();
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
      `Templates required in "${sendingGroupIdWithMissingTemplates}" routing config not found`
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
