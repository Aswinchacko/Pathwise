const logger = require('../utils/logger');

module.exports = function requestLogger(req, res, next) {
  const start = Date.now();
  res.on('finish', () => {
    const durationMs = Date.now() - start;
    logger.info(`${req.method} ${req.originalUrl} ${res.statusCode} - ${durationMs}ms`);
  });
  next();
};
