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

  if (!req.body.sendingGroupId) {
      sendError(res, 400, "Missing sendingGroupId");
      next();
      return;
  }

  if (!req.body.requestRefId) {
      sendError(res, 400, "Missing requestRefId");
      next();
      return;
  }

  if (!Array.isArray(req.body.data)) {
      sendError(res, 400, "Missing data array");
      next();
      return;
  }

  const requestItemRefIds = req.body.data.map(
      (item) => item.requestItemRefId
  );

  if (requestItemRefIds.includes(undefined)) {
      sendError(res, 400, 'Missing requestItemRefIds');
      next();
      return;
  }

  if (new Set(requestItemRefIds).size !== requestItemRefIds.length) {
      sendError(res, 400, 'Duplicate requestItemRefIds');
      next();
      return;
  }

  if (!validSendingGroupIds[req.body.sendingGroupId]) {
      sendError(res, 404, `Routing Config does not exist for clientId "sandbox_client_id" and sendingGroupId "${req.body.sendingGroupId}"`);
      next();
      return;
  }

  if (req.body.sendingGroupId === invalidRoutingPlanId) {
    sendError(res, 400, "Invalid Routing Config");
    next();
    return;
  }

  if (req.body.sendingGroupId === trigger425SendingGroupId) {
    sendError(res, 425, "Message with this idempotency key is already being processed");
    next();
    return;
}

  if (req.body.sendingGroupId === sendingGroupIdWithMissingNHSTemplates) {
      sendError(res, 500, `NHS App Template does not exist with internalTemplateId: invalid-template`);
      next();
      return;
  }

  if (req.body.sendingGroupId === sendingGroupIdWithMissingTemplates) {
      sendError(res, 500, `Templates required in "${req.body.sendingGroupId}" routing config not found`);
      next();
      return;
  }

  if (req.body.sendingGroupId === sendingGroupIdWithDuplicateTemplates) {
      sendError(res, 500, `Duplicate templates in routing config: ${JSON.stringify(duplicateTemplates)}`);
      next();
      return;
  }

  if (req.body.sendingGroupId === trigger500SendingGroupId) {
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
      requestId: KSUID.randomSync(new Date()).string
  });
  res.end();
  next();
}

module.exports = {
  batch_send
}
