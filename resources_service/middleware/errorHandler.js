const logger = require('../utils/logger');

module.exports = function errorHandler(err, req, res, next) {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';
  logger.error('Unhandled error:', { status, message, stack: err.stack });
  res.status(status).json({ error: message });
};

