var winston = require('winston');
var logger = winston.createLogger({
  transports: [
      new winston.transports.File({
          level: 'info',
          filename: './logs/all-logs.log',
          handleExceptions: true,
          format: winston.format.simple(),
          maxsize: 5242880, //5MB
          maxFiles: 5,
      }),
      new winston.transports.Console({
          level: 'error',
          handleExceptions: true,
          format: winston.format.cli()
      })
  ],
  exitOnError: false
});
logger.stream = {
  write: function(message, encoding){
      logger.info(message.trim());
  }
};

module.exports = logger;