module.exports = function handleError(err, req, res, next) {
  console.error(err)
  return res.status(500).json({ errors: [err.message] })
}