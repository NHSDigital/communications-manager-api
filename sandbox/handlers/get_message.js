import * as  fs from 'fs'
import { sendError, writeLog } from './utils.js'

export async function getMessage(req, res, next) {
  if (req.headers.authorization === "banned") {
    sendError(res, 403, "Request rejected because client service ban is in effect");
    next();
    return;
  }

  const { messageId } = req.params;

  fs.readFile(`./messages/${messageId}.json`, 'utf8', (err, fileContent) => {
    if (err) {
      writeLog(res, "warn", {
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
  });
}
