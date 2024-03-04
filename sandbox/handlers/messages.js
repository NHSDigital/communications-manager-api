const KSUID = require("ksuid");
const { sendError, write_log, hasValidGlobalTemplatePersonalisation } = require("./utils");
const {
  sendingGroupIdWithMissingNHSTemplates,
  sendingGroupIdWithMissingTemplates,
  sendingGroupIdWithDuplicateTemplates,
  duplicateTemplates,
  trigger500SendingGroupId,
  validSendingGroupIds,
  globalFreeTextNhsAppSendingGroupId,
} = require("./config");

async function messages(req, res, next) {
  if (req.headers["authorization"] === "banned") {
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

  const routingPlanId = req.body.data.attributes.routingPlanId;
  if (!validSendingGroupIds[routingPlanId]) {
    sendError(
      res,
      404,
      `Routing Config does not exist for clientId "sandbox_client_id" and routingPlanId "${req.body.data.attributes.routingPlanId}"`
    );
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

  write_log(res, "warn", {
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

module.exports = {
  messages,
};
