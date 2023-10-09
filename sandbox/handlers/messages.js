const KSUID = require("ksuid");
const { sendError, write_log } = require('./utils')

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
