#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

#蓝图，后台管理，构建在：/admin

#引入蓝图使用的模块
from flask import Blueprint,request,session,url_for,render_template
# 引入项目的常用方法模块，整个模块的导入需要从包开始: shopme.project_utils
import shopme.project_utils as pju
# 引入数据库操作模块中的相关方法
from .db_oper import admin_findByUP,admin_tadmin_findById
#引入 sqlite3模块，操作数据库
import sqlite3


# 创建蓝图对象
admin = Blueprint('admin',__name__)


# route路由对象，可以设置方法：methods=['GET','POST']，不设置默认为GET
#定义网站的主页
@admin.route('/')
def index():
	# 判断 session 中是否有登入对象 login_admin
	login_admin = session.get('login_admin')
	
	# 如果不存在，则返回到登入页面
	if login_admin is None:
		print('1111111111111111111111111111')
		return render_template('admin_login.html')
	else:
		print('2222222222222222222222')
		# 如果存在，表示已经登入状态了，则返回到管理员的主页面
		# 返回的时候，将登入信息带过去
		return render_template('admin_main.html',login_admin=login_admin)
	
#产生4位的验证码
@admin.route('/gnrcheckcode.do')
def gnrcheckcode():
	#产生一个4位验证码，大写
	check_code = pju.gnr_check_code()
	#放入到session中
	session['check_code']=check_code
	#返回json格式的验证码给前端
	return pju.to_json(check_code=check_code)
	
	
#登入的判断，只能是post方式
@admin.route('/login.do',methods=['POST'])
def login():
	#获得传递过来的页面参数
	username = request.form['username']
	password = request.form['password']
	checkcode = request.form['checkcode']
	
	# 判断验证码是否正确
	# 使用页面传递过来的验证码和session中的验证码进行比较
	# 页面传过来的验证码需要先转大写
	if checkcode.upper() != session.get('check_code'):
		return pju.to_json(succ=False,stmt='验证码不正确')
		
	# 进行数据库的验证
	login_admin = admin_findByUP(username,password)
	if login_admin is None:
		return pju.to_json(succ=False,stmt='用户名不存在或者密码错误')
		
	# 验证成功后，将管理员对象放入到 session
	session['login_admin'] = login_admin
	
	#返回登入成功信息
	return pju.to_json(succ=True)
	
# 退出，从 session 中移除 login_admin
@admin.route('/logout.do')
def logout():
	# pop 表示从 session 中移出一个对象，没有则默认返回 None
	session.pop('login_admin',None)
	return pju.to_json(succ=True)
	

# ===============================================
# 管理员数据表增删改查相关的操作
# ===============================================
# 打开页面模板：tadmin/page.html
@admin.route('/tadmin_page.do',methods=['GET','POST'])
def tadmin_page():
	login_admin = session.get('login_admin')
	if login_admin is None:
		return render_template('admin_login.html')
		
	# 跳转到 admin_tadmin_page.html，把查询结果和翻页数据带过去
	# 接受查询相关几个参数，必须是post过来的
	if request.method == 'POST':
		keyword = request.form['keyword']
		page = int(request.form['page'])
		pagesize = int(request.form['pagesize'])
	else:
		# 默认情况，几个查询参数赋初始值
		keyword=''
		page=1
		pagesize=10
		
	# data_modal 对象，字典，表示要传递到页面去的数据内容
	data_modal = {}
	# 从页面传递过来的几个参数也需要带回去，用于页面查询条件的填充
	data_modal['keyword']=keyword
	data_modal['page']=page
	data_modal['pagesize']=pagesize
	
		
	#首先查询总的数量，直接使用数据库链接查询
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	# dt_conn 用来存放 sql 中的占位符数据，字典
	dt_conn = {}
	# 组装sql语句，超级管理员记录不要查询
	sql = 'select count(*) from tadmin where type<9'
	if keyword!='':
		sql += ' and (code like :keyword or name like :keyword)'
		dt_conn['keyword']='%'+keyword+'%'
	
	print('sql=',sql)
	
	result_one = cursor.execute(sql,dt_conn).fetchone()
	# 满足条件的记录总数
	total = result_one[0] if (result_one is not None) else 0
	data_modal['total']=total
	
	if total>0:
		# 当记录总数大于0的时候，继续查询本页数据
		sql = 'select id,code,name,username,type from tadmin where type<9'
		if keyword!='':
			sql += ' and (code like :keyword or name like :keyword)'
			dt_conn['keyword']='%'+keyword+'%'
		# 末尾加上排序和翻页语法
		sql += ' order by code'
		# sqlite数据库中的分页语法：limit 10 offset 0
		sql += ' limit '+str(pagesize)+' offset '+str((page-1)*pagesize)
		print('sql=',sql)
		
		# 返回查询的所有数据，组装 rows 对象，列表，内部字典
		rows = []
		result_all = cursor.execute(sql,dt_conn).fetchall()
		for line in result_all:
			record = {};
			record['id']=line[0]
			record['code']=line[1]
			record['name']=line[2]
			record['username']=line[3]
			record['type']=line[4]
			rows.append(record)
			
		data_modal['rows']=rows
		
		#计算总共有多少页
		totalpage = total // pagesize
		if total % pagesize != 0:
			totalpage+=1
		data_modal['totalpage']=totalpage
		
		#翻页显示前三后三，需要使用列表
		pagenumbers=[]
		for i in range(page-3,page+4):
			if i<1:
				continue
			if i>totalpage:
				continue
			pagenumbers.append(i)
		data_modal['pagenumbers']=pagenumbers
	
	conn.close()
	
	return render_template('admin_tadmin_page.html',login_admin=login_admin,data_modal=data_modal)
	
# 新增或修改前，根据id号获得数据记录
@admin.route('/tadmin_presave.do',methods=['GET','POST'])
def tadmin_presave():
	# 必须有id参数，表示数据库记录的id号，get和post或者参数的方式不一样，需要区分
	if request.method == 'POST':
		id = int(request.form['id']) if ('id' in request.form) else 0
	else:
		id = int(request.args['id']) if ('id' in request.args) else 0
		
	if id==0:
		#新增的情况，构造默认的 数据记录
		record = {};
		record['id']=0
		record['code']=''
		record['name']=''
		record['username']=''
		record['type']=1
	else:
		#修改的情况，根据id号去找到数据库记录
		record = admin_tadmin_findById(id)
		if record is None:
			return pju.to_json(succ=False,stmt='无法找到记录. id={}'.format(id))
			
	#返回结果
	return pju.to_json(succ=True,record=record)
	
#tadmin 保存数据库
@admin.route('/tadmin_save.do',methods=['POST'])
def tadmin_save():
	# 获得参数
	id = int(request.form['id'])
	code = request.form['code']
	name = request.form['name']
	username = request.form['username']
	type = int(request.form['type'])
	
	# 开始数据库操作，保存之前，需要判断 code和username是否已经存在了
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	# 判断code是否存在
	sql = 'select count(*) from tadmin where id<>? and code=?'
	result_one = cursor.execute(sql,(id,code)).fetchone()
	total = result_one[0] if (result_one is not None) else 0
	if total>0:
		# 已经存在，错误，注意，返回之前数据库链接必须断开
		conn.close()
		return pju.to_json(succ=False,stmt='工号已经存在. code={}'.format(code))
	
	# 判断username是否存在
	sql = 'select count(*) from tadmin where id<>? and username=?'
	result_one = cursor.execute(sql,(id,username)).fetchone()
	total = result_one[0] if (result_one is not None) else 0
	if total>0:
		# 已经存在，错误，注意，返回之前数据库链接必须断开
		conn.close()
		return pju.to_json(succ=False,stmt='登入名已经存在. username={}'.format(username))
		
	
	# 根据id来判断是新增还是修改
	if id==0:
		#新增，密码默认是：123456 的md5加密
		password = pju.md5_encode('123456')
		# 插入数据库
		sql = 'insert into tadmin(code,name,username,password,type) values(?,?,?,?,?)';
		cursor.execute(sql,(code,name,username,password,type))
	else:
		# 修改，原来的密码不要变化
		sql = 'update tadmin set code=?,name=?,username=?,type=? where id=?';
		cursor.execute(sql,(code,name,username,type,id))
		
	# insert 和 update 都改变了数据库记录，需要执行提交
	conn.commit()
	conn.close()
	
	#返回成功
	return pju.to_json(succ=True)
		
	
# tadmin 删除
@admin.route('/tadmin_del.do',methods=['GET','POST'])
def tadmin_del():
	id = int(request.form['id'])
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	sql = 'delete from tadmin where id=?'
	cursor.execute(sql,(id,))
	conn.commit()
	conn.close()
	return pju.to_json(succ=True)
	
# tadmin 密码重置
@admin.route('/tadmin_resetpwd.do',methods=['GET','POST'])
def tadmin_resetpwd():
	id = int(request.form['id'])
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	sql = 'update tadmin set password=? where id=?'
	password = pju.md5_encode('123456')
	cursor.execute(sql,(password,id))
	conn.commit()
	conn.close()
	return pju.to_json(succ=True)
	
	
	
	
	
	