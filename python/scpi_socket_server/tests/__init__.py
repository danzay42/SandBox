import logging

if __debug__ is True:
	logger = logging.getLogger('debug')
else:
	logger = logging.getLogger('release')
