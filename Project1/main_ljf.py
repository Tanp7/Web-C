#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

import os
from unittest import result
from colorama import Cursor
from flask import Flask,request,render_template

from project_utils import get_db_path, to_json
import sqlite3

# 引入蓝图
# from bp_1 import bp1

cur_dir = os.path.dirname(os.path.abspath(__file__))
if cur_dir.find('\\')!=-1:
	cur_dir = cur_dir.replace('\\','/')

dir_static = cur_dir+'/static'
dir_templates = cur_dir+'/templates'

app = Flask(__name__,
	template_folder = dir_templates,
	static_folder = dir_static,
	static_url_path = ''
		)
		
# 注册蓝图
# app.register_blueprint(blueprint=bp1,url_prefix='/bp1')
		
@app.route('/test',methods=['GET','POST'])
def test():
	
	a=1
	b=3.14
	c='hello,你好'
	d=['111','222','3333']
	e={
		'code':'123456',
		'name':'张三',
		'age':20
	}
	
	return render_template('test.html',a1=a,b=b,c=c,d=d,e=e)
	
		
import xlrd
# 读取excel中的学生成绩
def read_excel_data():
	workbook = xlrd.open_workbook('./电商19A-学生成绩分析.xls')
	sheet = workbook.sheet_by_index(0)
	
	# 读取到全部的数据，二维列表
	data = []
	for i in range(1,40):
		row = sheet.row_values(i)
		data.append(row)
		
	return data
	
@app.route('/excel',methods=['GET','POST'])
def show_excel_data():

	# 接收参数
	if request.method=='POST':
		kw = request.form.get('kw') if ('kw' in request.form) else ''
		yy = request.form.get('yy') if ('yy' in request.form) else ''
		sx = request.form.get('sx') if ('sx' in request.form) else ''
		jsj = request.form.get('jsj') if ('jsj' in request.form) else ''
	else:
		# get 方式下，几个变量都设置为默认值
		kw = ''
		yy = ''
		sx = ''
		jsj = ''
		
	# 转换参数
	try:
		yy = float(yy)
		sx = float(sx)
		jsj = float(jsj)
	except:
		yy = 0.0
		sx = 0.0
		jsj = 0.0
		
	# 全部的数据，需要根据条件去筛选符合的那些
	data_all = read_excel_data()
	
	# 符合条件的数据
	data = []
	
	if kw!='':
		# 有关键字，则根据关键字进行查询
		for row in data_all:
			xuehao = row[0]
			xingming = row[1]
			if xuehao.find(kw)!=-1 or xingming.find(kw)!=-1:
				data.append(row)
	elif yy>0 or sx>0 or jsj>0:
		# 没有关键字的时候，判断是否有指定分数查询
		for row in data_all:
			if row[2]<yy or row[3]<sx or row[4]<jsj:
				data.append(row)
	else:
		# 没有指定查询条件，返回所有的
		data = data_all
	
	return render_template('excel.html',data=data)
	
@app.route('/f1')
def f1():
	return render_template('f2.html')
	
@app.route('/bs')
def bs():
	return render_template('bs.html')
	
# 显示数据库表 ztest 中的记录
@app.route('/ztest_list_ljf',methods=['GET','POST'])
def ztest_list_ljf():
	if request.method=='POST':
		kw = request.form.get('kw') if ('kw' in request.form) else ''
	else:
		kw = ''
		
	# 将页面上需要的数据统一放到数据模型 data modal 中,字典
	dm = {}
	dm['kw']=kw


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
	# print('result_one ', result_one)
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
			
		# print(sql)
		
		result = cursor.execute(sql,dt_conn).fetchall()
			
		dm['rows']=result
		# print(result)
		
	# 关闭数据库
	conn.close()
		
	return render_template('ztest_list_ljf.html',dm=dm)

# 增加修改前，获得数据内容

##--------------------
##--------zzh---------
##--------------------

@app.route('/remove', methods = ['POST','GET'])
def solve():
	id = request.form.get('id') if('id' in request.form) else ''
	try:
		id = int(id)
	except:
		id = 0
	print("id=",id)
	conn = sqlite3.connect(get_db_path())
	cursor = conn.cursor()
	sql = '''
	DELETE FROM ztest WHERE id = ?
	'''
	cursor.execute(sql,(id,))
	conn.commit()
	conn.close()
	return to_json(succ=True)

##--------------------
##--------zzh---------
##--------------------

@app.route('/presave',methods=['POST'])
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
@app.route('/save',methods=['POST'])
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
	
	# print('id, code, name, age, salary= ', id, code, name, age, salary)
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
	

if __name__ == '__main__':
	app.run(debug=True)
