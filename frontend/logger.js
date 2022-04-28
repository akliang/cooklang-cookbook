var winston = require('winston');

//
// winston helpers and setup
//
const maxSize = 1000000, maxFiles = 5

const myFormat = winston.format.printf( info => {
  return `${info.timestamp} [${info.level}]: (${info.metadata.service}) ${info.message}`;
});

const onlyHttp = winston.format((info, opts) => {
  if (info.level == 'http') { return info; }
  else { return false; }
});

const onlyError = winston.format((info, opts) => {
  if (info.level == 'error') { return info; }
  else { return false; }
});

const onlyWarn = winston.format((info, opts) => {
  if (info.level == 'warn') { return info; }
  else { return false; }
});

//
// actual winston logger
//
var logger = winston.createLogger({
  transports: [
      new winston.transports.File({
        level: 'http',
        filename: './logs/http.log',
        handleExceptions: true,
        format: winston.format.combine(
          onlyHttp(),
          winston.format.align(),
          winston.format.simple(),
        ),
        maxSize: maxSize,
        maxFiles: maxFiles,
      }),
      new winston.transports.File({
        level: 'error',
        filename: './logs/errors.log',
        handleExceptions: true,
        format: winston.format.combine(
          onlyError(),
          winston.format.align(),
          winston.format.metadata(),
          winston.format.timestamp(),
          myFormat,
        ),
        maxSize: maxSize,
        maxFiles: maxFiles,
      }),
      new winston.transports.File({
        level: 'warn',
        filename: './logs/warnings.log',
        handleExceptions: true,
        format: winston.format.combine(
          onlyWarn(),
          winston.format.align(),
          winston.format.metadata(),
          winston.format.timestamp(),
          myFormat,
        ),
        maxSize: maxSize,
        maxFiles: maxFiles,
      }),
      new winston.transports.Console({
          level: 'error',
          handleExceptions: true,
          format: winston.format.cli()
      })
  ],
  exitOnError: false
});

//
// apply special tag to morgan stream
//
logger.stream = {
  write: function(message, encoding){
      logger.log('http', message.trim());
  }
};

module.exports = logger;