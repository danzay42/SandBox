import logging.config
logging.config.dictConfig({
	'version': 1,
	'disable_existing_loggers': True,
	
	'formatters': {
		# 'experimental': {
		# 	'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		# 	'datefmt': '',
		# 	'style': '',
		# 	'validate': '',
		# },
		'brief': {
			'format': '%(asctime)s - %(levelname)s - %(message)s'
		},
		'default': {
			'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
			'datefmt': '%Y-%m-%d %H:%M:%S',
		},
		# 'precise': {
		# 	'format': '%(message)s',
		# 	'datefmt': '%Y-%m-%d %H:%M:%S',
		# },
	},
	
	# 'filters': {
	#
	# },
	
	'handlers': {
		# 'experimental': {
		# 	'class': 'logging.FileHandler',
		# 	'level': 'DEBUG',
		# 	'formatter': 'experimental',
		# 	'filters': ['default'],
		# 	'filename': 'experimental_handler_logger.log',
		# 	'maxBytes': 1024,
		# 	'backupCount': 3,
		# },
		'console': {
			'class': 'logging.StreamHandler',
			'formatter': 'brief',
			'stream': 'ext://sys.stdout',
		},
		'file': {
			'class': 'logging.FileHandler',
			'level': 'INFO',
			'encoding': 'utf-8',
			'formatter': 'default',
			'filename': 'experimental_handler_logger.log',
		},
		
	},
	
	'loggers': {
		'dev': {
			'handlers': ['console'],
			'propagate': False
		},
		'test': {
			'handlers': ['file'],
			'propagate': False
		},
		# 'root': {
		# 	'handlers': ['experimental'],
		# },
		'': {
			'level': 'DEBUG',
			'handlers': ['console', 'file'],
			'propagate': False
		},
		# '__main__': {
		# 	'handlers': ['console'],
		# 	'level': 'DEBUG',
		# 	'propagate': False
		# },
		'ppm_module': {
			'handlers': ['console', 'file'],
			'level': 'DEBUG',
			'propagate': False
		},
	}
})


if __name__ == '__main__':
	logger = logging.getLogger('dev')

	logger.debug("debug")
	logger.info("info")
	logger.warning("warning")
	logger.error("error")
	logger.critical("critical")
