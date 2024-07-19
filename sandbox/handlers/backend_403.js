export async function backend403(req, res, next) {
  res.status(403);
  res.send('{"message":"Forbidden"}');
  next();
}
