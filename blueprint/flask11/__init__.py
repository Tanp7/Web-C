#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 项目的说明

from flask import Flask
from flask11.project_utils import get_project_dir

from flask11.blueprint_test import t1
from flask11.blueprint_simple import simple

# 创建flask app 实例，以及配置蓝图模块
def create_app():
	app = Flask(__name__,
		template_folder = get_project_dir()+'/templates',
		static_folder = get_project_dir()+'/static',
		static_url_path = ''
	)
	
	# 配置蓝图
	app.register_blueprint(blueprint=t1)
	app.register_blueprint(blueprint=simple)
	return app
