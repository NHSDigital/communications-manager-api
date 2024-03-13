import * as  fs from 'fs'
import { sendError, write_log } from './utils.js'

export async function get_message(req, res, next) {
  if (req.headers["authorization"] === "banned") {
    sendError(res, 403, "Request rejected because client service ban is in effect");
    next();
    return;
  }

  const messageId = req.params.messageId;

  fs.readFile(`./messages/${messageId}.json`, 'utf8', (err, fileContent) => {
    if (err) {
      write_log(res, "warn", {
        message: `/api/v1/messages/${messageId}`,
        req: {
          path: req.path,
          query: req.query,
          headers: req.rawHeaders,
        }
      });
      sendError(res, 404, `Message with id of ${messageId} not found`);
      next();
      return
    }
    res.type('json').status(200).send(fileContent)
    return
  });
}
