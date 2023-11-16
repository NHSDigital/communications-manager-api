const { sendError, write_log } = require('./utils')
const { get_message_response_data } = require('./data')

async function get_message(req, res, next) {
  if (req.headers["authorization"] === "banned") {
    sendError(res, 403, "Request rejected because client service ban is in effect");
    next();
    return;
  }

  const messageId = req.params.messageId;


  get_message_response_data.forEach(({ messageId, body }) => {
    if (req.params.messageId === messageId) {
      res.status(200).json(body)
    }
  })

  write_log(res, "warn", {
    message: `/api/v1/messages/${messageId}`,
    req: {
      path: req.path,
      query: req.query,
      headers: req.rawHeaders,
      payload: req.body
    }
  });

  sendError(res, 404, `Message with id of ${messageId} not found`);
  next();
  return;
}

module.exports = {
  get_message
}
