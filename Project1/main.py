#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

import os
from flask import Flask,request,render_template

# 引入蓝图
# from bp_1 import bp1

cur_dir = os.path.dirname(os.path.abspath(__file__))
print('cur_dir=', cur_dir)
if cur_dir.find('\\')!=-1:
	cur_dir = cur_dir.replace('\\','/')
print('cur_dir=', cur_dir)

dir_static = cur_dir+'/static'
dir_templates = cur_dir+'/templates'
print('dir_templates=', dir_templates)

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

@app.route('/html')
def simple_html():
	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>hi</title>
</head>
<body>
html
</body>
</html>
	'''
	return html
    
@app.route('/test2',methods=['GET','POST'])	
def test2():
    html = render_template('test2.html')
    return html
    
@app.route('/test3',methods=['GET','POST'])	
def test3():
    v1 = 110
    html = render_template('test3.html', a1=v1)
    return html
# -----------------------------------------
# 郑子涵
# -----------------------------------------
import xlrd
# 读取excel中的学生成绩
def read_excel_data():
	workbook = xlrd.open_workbook('./电商19A-学生成绩分析.xls')
	sheet = workbook.sheet_by_index(0)
	
	# 读取到全部的数据，二维列表
	data = []
	for i in range(0,40):
		row = sheet.row_values(i)
		data.append(row)
		
	return data
@app.route('/wawa',methods=['GET', 'POST'])
def kan():
	return render_template('nop.html', data = read_excel_data())

# -----------------------------------------
# -----------------------------------------

@app.route('/excel',methods=['GET','POST'])
def show_excel_data():
	pass	
	
@app.route('/f1')
def f1():
	return render_template('f2.html')
		
if __name__ == '__main__':
	app.run(debug=True)
