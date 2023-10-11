async function backend_504(req, res, next) {
  res.status(504);
  res.send("504 Gateway Timeout");
  next();
}

module.exports = {
  backend_504
}
