#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

import logging
from shopme import create_app

app = create_app()

#如果不是自己启动，那么就使用gunicorn的日志
if __name__ != '__main__':
	gunicorn_logger = logging.getLogger('gunicorn.error')
	app.logger.handlers = gunicorn_logger.handlers
	app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
	app.run(debug=True,port=5005)