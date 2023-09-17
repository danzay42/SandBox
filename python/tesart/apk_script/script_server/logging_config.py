import os
import logging.config
import logging


def get_config_logger(name=None, path=None):
	path = path or os.path.dirname(__file__) + '/../'
	config = {
		'version': 1,
		'disable_existing_loggers': True,

		'formatters': {
			'brief': {
				'format': '%(asctime)s %(levelname)s: %(message)s',
			},
			'default': {
				'format': '%(asctime)s %(levelname)s: %(message)s',
			},
			'precise': {
				'format':
					'%(asctime)s %(levelname)s [%(name)s|%(module)s|%(filename)s|%(funcName)s|%(lineno)d]: %(message)s',
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
				'filename': path + 'debug.record.log',
				'mode': 'w',
				'maxBytes': 1_000000,
				'backupCount': 3,
			},
			'file_last': {
				'class': 'logging.FileHandler',
				'level': 'INFO',
				'encoding': 'utf-8',
				'formatter': 'brief',
				'filename': path + 'last.record.log',
				'mode': 'w',
			},
			'file_errors': {
				'class': 'logging.FileHandler',
				'level': 'ERROR',
				'encoding': 'utf-8',
				'formatter': 'precise',
				'filename': path + 'errors.record.log',
				'mode': 'w',
			}
		},

		'loggers': {
			'debug': {
				'handlers': ['console', 'file', 'file_last', 'file_errors'],
				'level': 'DEBUG',
				'propagate': False
			},
			'antest_v2': {
				'handlers': ['console', 'file', 'file_last', 'file_errors'],
				'level': 'INFO',
				'propagate': False
			},
		}
	}

	logging.config.dictConfig(config)
	return logging.getLogger(name or 'debug')


if __name__ == '__main__':
	logger = get_config_logger('debug')
	logger.debug(f"debug")
	logger.info(f"info")
	logger.warning(f"warning")
	logger.error(f"error")
	logger.critical(f"critical")
