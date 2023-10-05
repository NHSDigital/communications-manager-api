async function status(req, res, next) {
  res.json({
      status: "pass",
      ping: "pong",
      service: req.app.locals.app_name,
      version: req.app.locals.version_info
  });
  res.end();
  next();
}

module.exports = {
  status
}
