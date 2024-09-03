export async function backend504(req, res, next) {
  res.status(504);
  res.send("504 Gateway Timeout");
  next();
}
