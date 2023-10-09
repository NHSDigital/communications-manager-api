async function trigger_timeout(req, res, next) {
  let timeoutLength = 3000;

  if (req.query.sleep) {
      timeoutLength = parseInt(req.query.sleep);
  }

  setTimeout(() => {
      res.status(200);
      res.json({});
      next();
  }, timeoutLength);
}

module.exports = {
  trigger_timeout
}
