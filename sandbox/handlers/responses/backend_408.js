export async function backend408(req, res, next) {
  res.status(408);
  res.send("408 Request Timeout");
  next();
}
