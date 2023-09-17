import os
import logging.config
import logging

LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    
    'formatters': {
        'brief': {
            'format': '%(asctime)s %(levelname)s: %(message)s'
        },
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s'
        },
        'precise': {
            'format': '[%(levelname)s]-%(asctime)s %(name)s|%(module)s|%(filename)s|%(funcName)s|%(lineno)d: %(message)s',
        },
    },
    
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'brief',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'brief',
            'encoding': 'utf-8',
            'filename': os.path.dirname(__file__) + './../debug.record.log',
            'mode': 'w',
            'maxBytes': 1_000000,
            'backupCount': 3,
        },
        'file_last': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'encoding': 'utf-8',
            'formatter': 'default',
            'filename': os.path.dirname(__file__) + './../last.record.log',
            'mode': 'w',
        }
    },
    
    'loggers': {
        'debug': {
            'handlers': ['console', 'file', 'file_last'],
            'level': 'DEBUG',
            'propagate': False
        },
        'release': {
            'handlers': ['console', 'file', 'file_last'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

logging.config.dictConfig(LOGCONFIG)
if __debug__ is True:
    logger = logging.getLogger('debug')
else:
    logger = logging.getLogger('release')


if __name__ == '__main__':
    logging.config.dictConfig(LOGCONFIG)
    for logger_name in ['debug', 'release']:
        logger = logging.getLogger(logger_name)
        logger.debug(f"logger:{logger_name} debug")
        logger.info(f"logger:{logger_name} info")
        logger.warning(f"logger:{logger_name} warning")
        logger.error(f"logger:{logger_name} error")
        logger.critical(f"logger:{logger_name} critical")
