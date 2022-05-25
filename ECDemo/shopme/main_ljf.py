#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

import os
from flask import Flask,request,render_template

from flask import Blueprint,request,session,url_for,render_template
import shopme.project_utils as pju

from shopme.project_utils import get_db_path, to_json
import sqlite3

# 引入蓝图
# from bp_1 import bp1

# 创建蓝图对象
main_ljf = Blueprint('main_ljf',__name__)
		
# 显示数据库表 ztest 中的记录
@main_ljf.route('/ztest_list_ljf',methods=['GET','POST'])
def ztest_list_ljf():
	if request.method=='POST':
		kw = request.form.get('kw') if ('kw' in request.form) else ''
		
		# 翻页的两项
		page = request.form.get('page') if ('page' in request.form) else '1'
		pagesize = request.form.get('pagesize') if ('pagesize' in request.form) else '2'
	else:
		kw = ''
		page='1'
		pagesize='2'
		
	try:
		page = int(page)
		pagesize = int(pagesize)
	except:
		page=1
		pagesize=3
		
	# 将页面上需要的数据统一放到数据模型 data modal 中,字典
	dm = {}
	dm['kw']=kw
	dm['page']=page
	dm['pagesize']=pagesize


	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()
	
	# 定义一个查询条件的字典
	dt_conn = {}
	
	# 翻页需要先找到满足条件的记录有多少条
	sql = '''
	select count(*) from ztest where 1=1
	'''
	if kw!='':
		sql += ' and name like :kw'
		dt_conn['kw']='%'+kw+'%'
		
	result_one = cursor.execute(sql,dt_conn).fetchone()
	print('result_one ', result_one)
	# 满足条件的记录总数
	total = result_one[0] if (result_one is not None) else 0
	dm['total']=total
	
	# 本页数据内容的查询，当 total>0 时进行
	if total>0:
	
		sql = '''
		select * from ztest where 1=1
		'''
		
		if kw!='':
			sql += ' and name like :kw'
			dt_conn['kw']='%'+kw+'%'
			
		# 加上翻页的sql
		sql += ' limit '+str(pagesize)+' offset '+str((page-1)*pagesize)
			
		print(sql)
		
		result = cursor.execute(sql,dt_conn).fetchall()
			
		dm['rows']=result
		
		#计算总共有多少页
		totalpage = total // pagesize
		if total % pagesize != 0:
			totalpage+=1
		dm['totalpage']=totalpage
		
		#翻页显示前三后三，需要使用列表
		pagenumbers=[]
		for i in range(page-3,page+4):
			if i<1:
				continue
			if i>totalpage:
				continue
			pagenumbers.append(i)
			
		print(pagenumbers)
		
		dm['pagenumbers']=pagenumbers
		

	# 关闭数据库
	conn.close()
		
	return render_template('ztest_list_ljf.html',dm=dm)

# 删除
@main_ljf.route('/remove',methods=['POST'])
def remove():
	id = request.form.get('id') if ('id' in request.form) else ''
	
	try:
		id = int(id)
	except:
		id = 0
		
	# 删除必须根据id号
	if id>0:
		conn = sqlite3.connect(get_db_path())
		cursor = conn.cursor()
		sql = '''
		delete from ztest where id=?
		'''
		cursor.execute(sql,(id,))
		conn.commit()
		conn.close()
		
	# json形式返回成功
	return to_json(succ=True)

# 增加修改前，获得数据内容
@main_ljf.route('/presave',methods=['POST'])
def presave():
	# 数据库记录的id号，>0表示修改
	id = request.form.get('id') if ('id' in request.form) else ''
	try:
		id = int(id)
	except:
		id = 0
		
	# 返回给页面的，一条数据记录，指定默认值
	# 新增的情况，返回默认值
	record = {}
	record['id']=0
	record['code']=0
	record['name']=''
	record['age']=0
	record['salary']=''
	
	
	if id>0:
		# 修改的情况，需要从数据库获得记录的数据
		conn = sqlite3.connect(get_db_path())
		cursor = conn.cursor()
		sql = '''
		select * from ztest where id=?
		'''
		result_one = cursor.execute(sql,(id,)).fetchone()
		if result_one is not None:
			record['id']=result_one[0]
			record['code']=result_one[1]
			record['name']=result_one[2]
			record['age']=result_one[3]
			record['salary']=result_one[4]
			
			
		conn.close()
		
	# 以json数据的形式返回
	return to_json(succ=True,record=record)
	
# 保存数据库
@main_ljf.route('/save',methods=['POST'])
def save():
	id = request.form.get('id') if ('id' in request.form) else ''
	code = request.form.get('code') if ('code' in request.form) else ''
	name = request.form.get('name') if ('name' in request.form) else ''
	age = request.form.get('age') if ('age' in request.form) else ''
	salary = request.form.get('salary') if ('salary' in request.form) else ''

	
	try:
		id = int(id)
	except:
		id = 0
	
	print('id, code, name, age, salary= ', id, code, name, age, salary)
	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()
		
	if id>0:
		# 修改
		sql = '''
		update ztest set code=?,name=?,age=?,salary=? where id=?
		'''
		cursor.execute(sql,(code,name,age,salary,id))
	else:
		# 新增
		sql = '''
		insert into ztest(code,name,age,salary) 
		values(?,?,?,?)
		'''
		cursor.execute(sql,(code,name,age,salary))
		
	conn.commit()
	conn.close()
	
	# json形式返回成功
	return to_json(succ=True)
