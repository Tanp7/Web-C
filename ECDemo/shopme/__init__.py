#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# shopme 项目，经典的电子商务网站设计开发

import os
from flask import Flask

#导入蓝图的对象，需要进行注册的
from .bp_main import main
from .bp_admin import admin
from .main_ljf import main_ljf
from .bp_product import product
from .bp_dayspecial import dayspecial
from .bp_newarrival import newarrival
from .idol import idol
# 引入数据库操作模块中的数据库初始化
from .db_oper import init_database

#定义项目的基本配置
project_config = {}

# 项目启动时候执行的方法
def project_start():
	#数据库初始化
	init_database()
	


#初始化，创建app
def create_app():
	#构建项目路径文件夹
	#项目根目录
	tmpdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	if tmpdir.find('\\')!=-1:
		tmpdir = tmpdir.replace('\\','/')
	project_config['BASE_DIR'] = tmpdir
	#静态文件和模板存放的目录
	tmpdir = os.path.join(project_config['BASE_DIR'], __name__,'static')
	if tmpdir.find('\\')!=-1:
		tmpdir = tmpdir.replace('\\','/')
	project_config['STATIC_DIR'] = tmpdir
	tmpdir = os.path.join(project_config['BASE_DIR'],__name__, 'templates')
	if tmpdir.find('\\')!=-1:
		tmpdir = tmpdir.replace('\\','/')
	project_config['TEMPLATES_DIR'] = tmpdir

	print('project_config:',project_config)
	
	

	#建立app对象
	# static_url_path: 访问静态资源时候默认的前缀是 /static, 设置为'', 则不需要写 /static了
	app = Flask(__name__,
		template_folder=project_config['TEMPLATES_DIR'],
		static_folder=project_config['STATIC_DIR'],
		static_url_path='')
	
	#注册蓝图
	#各个蓝图模块需要在此进行注册，如果蓝图有url的前缀，则：app.register_blueprint(profile, url_prefix='/<user_url_slug>')
	app.register_blueprint(blueprint=main)
	app.register_blueprint(blueprint=admin,url_prefix='/admin')
	app.register_blueprint(blueprint=main_ljf,url_prefix='/main_ljf')
	app.register_blueprint(blueprint=product,url_prefix='/product')
	app.register_blueprint(blueprint=dayspecial,url_prefix='/dayspecial')
	app.register_blueprint(blueprint=newarrival,url_prefix='/newarrival')
	app.register_blueprint(blueprint=idol,url_prefix='/idol')
	
	#为了使用 session，必须设置密钥
	app.secret_key = '\xaf\xdb\x8dS\xf6s\xa8\x93-t\xf6\x989K.\xcd>;R\n\x81\xfdP\xb0'
	
	#执行项目启动方法
	project_start()
	
	return app