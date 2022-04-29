var winston = require('winston');

//
// winston helpers and setup
//
const maxSize = 1000000;
const maxFiles = 5;
const customLevels = {
  levels: {
    httpsuccess: 0,
    httperror: 1,
    critical: 2,
    error: 3,
    warn: 4,
    notice: 5,
    info: 6,
    debug: 7
  },
  colors: {
    httpsuccess: 'green',
    httperror: 'red',
    critical: 'red',
    error: 'red',
    warning: 'yellow',
    notice: 'green',
    info: 'green',
    debug: 'green'
  }
};
winston.addColors(customLevels.colors);

const myFormat = winston.format.printf( info => {
  return `${info.timestamp} [${info.level}]: (${info.metadata.service}) ${info.message}`;
});

const onlyHttpSuccess = winston.format((info, opts) => {
  if (info.level == 'httpsuccess') { return info; }
  else { return false; }
});

const onlyHttpError = winston.format((info, opts) => {
  if (info.level == 'httperror') { return info; }
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

const onlyInfo = winston.format((info, opts) => {
  if (info.level == 'info') { return info; }
  else { return false; }
});

//
// actual winston logger
//
var logger = winston.createLogger({
  levels: customLevels.levels,
  transports: [
      new winston.transports.File({
        level: 'httpsuccess',
        filename: './logs/httpsuccess.log',
        handleExceptions: true,
        format: winston.format.combine(
          onlyHttpSuccess(),
          winston.format.align(),
          winston.format.simple(),
        ),
        maxSize: maxSize,
        maxFiles: maxFiles,
      }),
      new winston.transports.File({
        level: 'httperror',
        filename: './logs/httperror.log',
        handleExceptions: true,
        format: winston.format.combine(
          onlyHttpError(),
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
      new winston.transports.File({
        level: 'info',
        filename: './logs/infos.log',
        handleExceptions: true,
        format: winston.format.combine(
          onlyInfo(),
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
          format: winston.format.combine(
            onlyHttpError(),
            onlyError(),
            onlyWarn(),
            winston.format.cli()
          )
      })
  ],
  exitOnError: false
});

//
// apply special tag to morgan stream
//
logger.httpsuccess = {
  write: function(message, encoding){
      logger.log('httpsuccess', message.trim());
  }
};

logger.httperror = {
  write: function(message, encoding){
      logger.log('httperror', message.trim());
  }
};

module.exports = logger;