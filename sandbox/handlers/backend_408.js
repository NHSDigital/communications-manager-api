async function backend_408(req, res, next) {
  res.status(408);
  res.send("408 Request Timeout");
  next();
}

module.exports = {
  backend_408
}
