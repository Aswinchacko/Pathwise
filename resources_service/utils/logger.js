const winston = require('winston');
const path = require('path');

// Create logs directory if it doesn't exist
const fs = require('fs');
const logsDir = path.join(__dirname, '../logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

// Custom format for console output
const consoleFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.colorize(),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    let log = `${timestamp} [${level}]: ${message}`;
    if (Object.keys(meta).length > 0) {
      log += `\n${JSON.stringify(meta, null, 2)}`;
    }
    return log;
  })
);

// Custom format for file output
const fileFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

// Create the logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: fileFormat,
  defaultMeta: { service: 'resources-service' },
  transports: [
    // Write all logs with importance level of `error` or less to `error.log`
    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 5,
    }),
    
    // Write all logs with importance level of `info` or less to `combined.log`
    new winston.transports.File({
      filename: path.join(logsDir, 'combined.log'),
      maxsize: 5242880, // 5MB
      maxFiles: 5,
    }),
    
    // Write scraping-specific logs
    new winston.transports.File({
      filename: path.join(logsDir, 'scraping.log'),
      level: 'info',
      maxsize: 5242880, // 5MB
      maxFiles: 3,
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json(),
        winston.format.printf((info) => {
          // Only log scraping-related messages
          if (info.message && (
            info.message.includes('scraping') || 
            info.message.includes('Scraping') ||
            info.message.includes('🔍') ||
            info.message.includes('📡') ||
            info.message.includes('✅') ||
            info.message.includes('❌') ||
            info.message.includes('🎉')
          )) {
            return JSON.stringify(info);
          }
          return false;
        })
      ).transform((info) => info !== false ? info : false)
    })
  ],
  
  // Handle uncaught exceptions
  exceptionHandlers: [
    new winston.transports.File({
      filename: path.join(logsDir, 'exceptions.log')
    })
  ],
  
  // Handle unhandled promise rejections
  rejectionHandlers: [
    new winston.transports.File({
      filename: path.join(logsDir, 'rejections.log')
    })
  ]
});

// If we're not in production, log to the console as well
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: consoleFormat,
    level: 'debug'
  }));
}

// Add custom logging methods for scraping
logger.scraping = {
  start: (query, source) => {
    logger.info(`🔍 Starting scraping for "${query}" from ${source}`, {
      action: 'scraping_start',
      query,
      source,
      timestamp: new Date().toISOString()
    });
  },
  
  success: (query, source, count) => {
    logger.info(`✅ Successfully scraped ${count} resources for "${query}" from ${source}`, {
      action: 'scraping_success',
      query,
      source,
      count,
      timestamp: new Date().toISOString()
    });
  },
  
  error: (query, source, error) => {
    logger.error(`❌ Failed to scrape "${query}" from ${source}: ${error.message}`, {
      action: 'scraping_error',
      query,
      source,
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    });
  },
  
  complete: (query, totalResources, totalSources) => {
    logger.info(`🎉 Scraping completed for "${query}": ${totalResources} resources from ${totalSources} sources`, {
      action: 'scraping_complete',
      query,
      totalResources,
      totalSources,
      timestamp: new Date().toISOString()
    });
  }
};

// Add performance logging
logger.performance = {
  start: (operation) => {
    const startTime = Date.now();
    return {
      end: () => {
        const duration = Date.now() - startTime;
        logger.info(`⏱️  ${operation} completed in ${duration}ms`, {
          action: 'performance',
          operation,
          duration,
          timestamp: new Date().toISOString()
        });
        return duration;
      }
    };
  }
};

module.exports = logger;