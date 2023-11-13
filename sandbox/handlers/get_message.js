const KSUID = require("ksuid");
const { sendError, write_log } = require('./utils')

async function get_message(req, res, next) {
  if (req.headers["authorization"] === "banned") {
    sendError(res, 403, "Request rejected because client service ban is in effect");
    next();
    return;
  }

  const messageId = req.params.messageId;


  write_log(res, "warn", {
    message: `/api/v1/messages/${messageId}`,
    req: {
      path: req.path,
      query: req.query,
      headers: req.rawHeaders,
      payload: req.body
    }
  });

  const messageReference = KSUID.randomSync(new Date()).string
  const batchId = KSUID.randomSync(new Date()).string
  const routingPlanId = KSUID.randomSync(new Date()).string

  res.status(201).json({
    data: {
      type: 'Message',
      id: messageId,
      attributes: {
        messageStatus: "created",
        messageReference: messageReference,
        routingPlan: {
          id: routingPlanId,
          version: 1
        },
        channels: [],
        log: [],
        pdsMeta: [],
        timestamps: {
          created: new Date()
        }
      },
      links: {
        self: `%PATH_ROOT%/${messageId}`
      },
      relationships: {
        messageBatch: {
          data: {
            type: "MessageBatch",
            id: batchId
          }
        }
      }
    }
  });
  res.end();
  next();
}

module.exports = {
  get_message
}
