import os
import logging.config
import logging

LOGCONFIG = {
	'version': 1,
	'disable_existing_loggers': True,
	
	'formatters': {
		'brief': {
			'format': '%(asctime)s - %(levelname)s - %(message)s'
		},
		'default': {
			'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
			'datefmt': '%Y-%m-%d %H:%M:%S',
		},
		'precise': {
			'format': '[%(levelname)s]-%(asctime) s%(name)s|%(module)s|%(filename)s|%(funcName)s|%(lineno)d: %(message)s',
		},
	},
	
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'level': 'DEBUG',
			'formatter': 'brief',
			'stream': 'ext://sys.stdout',
		},
		'file': {
			'class': 'logging.FileHandler',
			'level': 'INFO',
			'encoding': 'utf-8',
			'formatter': 'default',
			'filename': os.path.dirname(__file__) + '/record.log',
			'mode': 'w',
		},
		'rotate_file': {
			'class': 'logging.handlers.RotatingFileHandler',
			'level': 'WARNING',
			'formatter': 'precise',
			'encoding': 'utf-8',
			'filename': os.path.dirname(__file__) + '/record.r.log',
			'mode': 'w',
			'maxBytes': 100000,
			'backupCount': 2,
		},
	},
	
	'loggers': {
		'debug': {
			'handlers': ['console', 'file'],
			'level': 'DEBUG',
			'propagate': False
		},
		'release': {
			'handlers': ['console', 'rotate_file'],
			'level': 'WARNING',
			'propagate': False
		},
	}
}


if __name__ == '__main__':
	logging.config.dictConfig(LOGCONFIG)
	for logger_name in ['debug', 'release']:
		logger = logging.getLogger(logger_name)
		logger.debug(f"logger:{logger_name} debug")
		logger.info(f"logger:{logger_name} info")
		logger.warning(f"logger:{logger_name} warning")
		logger.error(f"logger:{logger_name} error")
		logger.critical(f"logger:{logger_name} critical")
