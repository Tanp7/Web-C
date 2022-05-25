#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   : iceking  2020-2-1

# 数据库操作模块，sqlite3数据库，数据库名称：shopme.db

import os
#引入 sqlite3模块，操作数据库
import sqlite3

#获得当前文件夹，绝对路径
cur_dir = os.path.dirname(os.path.abspath(__file__))
#如果存在windows中的\\路径字符，需要替换为 /
if cur_dir.find('\\')!=-1:
	cur_dir = cur_dir.replace('\\','/')
#数据库文件的路径
db_path = cur_dir+'/shopme.db'
print('数据库文件路径：'+db_path)

#测试select语句
def test_select():
	#打开数据库链接
	conn = sqlite3.connect(db_path)
	#获得数据库访问的游标
	cursor = conn.cursor()
	#组装sql语句，select语句如果比较长，建议三个引号的多行字符串使用
	#sql语句可以使用占位符，问号? 或者名称 :name 方式，一般 ? 方式使用的较多
	# 使用 ? 作为占位符，第二个数据参数必须是：元组
	# 使用 :name 作为占位符，第二个参数必须是：字典
	sql = '''
	select * from ztest where name like :name
	'''
	# 返回查询的结果集对象
	# result_set.fetchone: 返回查询结果的第1条，元组
	# result_set.fetchall: 返回所有的结果，列表
	result_set = cursor.execute(sql,{'name':'%张%'})
	for row in result_set:
		print(row,type(row))
	
	#关闭本次链接，必须
	conn.close()
	
def test_insert():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	sql = '''
	insert into ztest(code,name,age) values(?,?,?)
	'''
	
	#insert,update,delte, 没有返回结果，直接执行即可
	cursor.execute(sql,('a0002','李四',25))
	
	#insert,update,delte, 必须做 提交
	conn.commit()
	
	conn.close()
	
def test_update():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	sql = '''
	update ztest set age=? where id=?
	'''
	cursor.execute(sql,(28,2))
	
	conn.commit()
	conn.close()
	
def test_delete():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	sql = '''
	delete from ztest where id=?
	'''
	# 注意，? 只有一个的时候，也需要元组形式，加逗号 ：(2,)
	cursor.execute(sql,(2,))
	
	conn.commit()
	conn.close()
	
	
if __name__ == '__main__':
	ls=['a','b','c','d']
	for i in range(len(ls)):
		print(ls[i],i)
	
	