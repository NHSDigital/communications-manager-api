const KSUID = require("ksuid");
const { sendError, write_log } = require('./utils')
const {
  sendingGroupIdWithMissingNHSTemplates,
  sendingGroupIdWithMissingTemplates,
  sendingGroupIdWithDuplicateTemplates,
  duplicateTemplates,
  trigger500SendingGroupId,
  validSendingGroupIds,
} = require('./config')

async function messages(req, res, next) {
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

  if (!validSendingGroupIds[req.body.data.attributes.routingPlanId]) {
      sendError(res, 404, `Routing Config does not exist for clientId "sandbox_client_id" and sendingGroupId "${req.body.data.attributes.routingPlanId}"`);
      next();
      return;
  }

  if (req.body.data.attributes.routingPlanId === sendingGroupIdWithMissingNHSTemplates) {
    sendError(res, 500, `NHS App Template does not exist with internalTemplateId: invalid-template`);
    next();
    return;
  }

  if (req.body.data.attributes.routingPlanId === sendingGroupIdWithMissingTemplates) {
    sendError(res, 500, `Templates required in "${sendingGroupIdWithMissingTemplates}" routing config not found`);
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
    message: "/api/v1/messages",
    req: {
      path: req.path,
      query: req.query,
      headers: req.rawHeaders,
      payload: req.body
    }
  });

  const messageId = KSUID.randomSync(new Date()).string

  res.status(201).json({
    data: {
      type: 'Message',
      id: messageId,
      attributes: {
        routingPlanId: req.body.data.attributes.routingPlanId,
        messageReference: req.body.data.attributes.messageReference,
        messageStatus: "created",
        timestamps: {
          created: new Date()
        }
      },
      links: {
        self: `%PATH_ROOT%/${messageId}`
      }
    }
  });
  res.end();
  next();
}

module.exports = {
  messages
}
