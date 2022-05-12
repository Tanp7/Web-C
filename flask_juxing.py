#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   : zzh

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
	return '欢迎访问我的主页'

@app.route('/hello')
def hello_world():
	html = '你好'
	return html

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


@app.route('/student')
def f1():
	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Title Here</title>
</head>
<body>
	'''
	print("{:.2f}".format(3.1415926))
	print("{} {}".format("hello", "world"))
	
	for i in range(10):
		html += '<p style="font-size:20px;color:red;">第一段</p>'
		
	html += '<p>学号：{}，姓名：{}</p>'.format('12345','张三')
		
	html += '''
</body>
</html>
	'''
	
	return html
	
import xlrd
# 读取excel中的学生成绩
def read_excel_data():
	workbook = xlrd.open_workbook('./电商19A-学生成绩分析.xlsx')
	sheet = workbook.sheet_by_index(0)
	
	# 读取到全部的数据，二维列表
	data = []
	for i in range(1,40):
		row = sheet.row_values(i)
		data.append(row)
		
	return data

@app.route('/excel')
def show_excel_data():
	data = read_excel_data()		
		
	# 组装html
	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title></title>
</head>
<body>
<input 
<p>
<form method="get" action="/excel">
姓名：<input type="text" name="a" value="{}">
<br>
<input type="submit" value="查询">
</form>
</p>

<table border="1">
		<td>学号</td>
		<td>姓名</td>
		<td>英语</td>
		<td>数学</td>
		<td>计算机</td>
	</tr>
	'''
	
	# 中间的tr需要循环
	for row in data:
		# tr中的相应位置挖槽填充
		tmp = '''
		<tr>
			<td>{}</td>
			<td>{}</td>
			<td>{}</td>
			<td>{}</td>
			<td>{}</td>
		</tr>
		'''
		
		html += tmp.format(row[0],row[1],row[2],row[3],row[4])
	html += '''
</table>

</body>
</html>
	'''
	
	return html


# ZZH HOMEWORK FOR THE CLASS IN THE 4.1
# --------------------------------------------------------------> 
from flask import request
@app.route('/search',methods=['GET','POST'])
def search():
	if request.method == 'POST':
		a = request.form.get('a')
	else:
		a = request.args.get('a')
	if a is None:
		a = ''
	data = read_excel_data()	
	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Title Here</title>
</head>
<body>

<form method="post" action="/search">
姓名：<input type="text" name="a" value="">
<input type="submit" value="查询">
</form>

<table border="1">
	<tr>
		<td>学号</td>
		<td>姓名</td>
		<td>英语</td>
		<td>数学</td>
		<td>计算机</td>
	</tr>
	'''
	for x in data:
		nop = row[1]
		if nop.rind(a) != -1 or a == '':
			tmp = '''
			<tr>
				<td>{}</td>
				<td>{}</td>
				<td>{}</td>
				<td>{}</td>
				<td>{}</td>
			</tr>
			'''
			html += tmp.format(x[0],x[1],x[2],x[3],x[4])
	html +='''
	</table>
	</body>
	</html>
	'''
	return html
# -------------------------------------------------->

# ====================================================================
# 参数的传递
# GET方式：request.args 字典
# POST方式：request.form 字典
# ====================================================================
@app.route('/p1',methods=['GET','POST'])
def test_param():
	# step1：接收页面传递过来的参数，区分get和post
	# step2：将各个参数转换为正确的类型，以及设置默认值与异常处理
	# step3：根据要求进行程序逻辑处理，得到结果数据结构，变量、列表、字典
	# step4：使用结果数据结构，组装 html
	pass
	
# ====================================================================
# 计算矩形面积
# ====================================================================
@app.route('/rectarea.do',methods=['GET','POST'])
def rectangle_area():
	if request.method == 'POST':
		a = request.form.get('a')
		b = request.form.get('b')
	else:
		a = request.args.get('a')
		b = request.args.get('b')
		
	if a is None:
		a='0'
	
	if b is None:
		b='0'
		
	# 参数一定默认是字符型，转换需要进行try
	try:
		a=int(a)
		b=int(b)
	except:
		a=0
		b=0
	print(request.method, a, b)
	html = '矩形长:{}, 宽：{}, 面积:{}'.format(a,b,a*b)
	#html.format(a,b,int(a)*int(b)) #format不能和原始字符串分开。
	#网页转圈刷新不出来时，在python文件运行的黑色窗口里，按回车。
	return html

@app.route('/rectarea2.do',methods=['GET','POST'])
def rectangle_area2():
	print(request.method)
	if request.method == 'POST':
		a = request.form.get('a')
		b = request.form.get('b')
	else:
		a = request.args.get('a')
		b = request.args.get('b')
		
	if a is None:
		a='0'
	
	if b is None:
		b='0'

	# 参数一定默认是字符型，转换需要进行try
	try:
		a=int(a)
		b=int(b)
	except:
		a=0
		b=0
		
	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Title Here</title>
</head>
<body>

<h1>矩形面积的计算</h1>
<p>
<form method="post" action="/rectarea2.do">
长：<input type="text" name="a" value="{}">
宽：<input type="text" name="b" value="{}">
<br>
<input type="submit" value="计算面积">

</form>
</p>

<h1>计算得到的面积为：{}</h1>

</body>
</html>
	
	'''.format(a,b,a*b)
	
	return html

# ====================================================================
# 计算矩形面积
# ====================================================================
@app.route('/rectarea3.do',methods=['GET'])
def rectangle_area3():
	a = 3;b=4;
	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Title Here</title>
</head>
<body>

<h1>矩形面积的计算</h1>
<p>
<form method="get" action="/rectarea3.do">
长：<input type="text" name="a" value="{}">
宽：<input type="text" name="b" value="{}">
<br>
<input type="submit" value="计算面积">

</form>
</p>

<h1>计算得到的面积为：{}</h1>

</body>
</html>
	
	'''.format(a,b,a*b)
	
	return html
 
@app.route('/rectarea4.do',methods=['GET'])
def rectangle_area4():
	a = request.args.get('a')
	b = request.args.get('b')
		
	if a is None:
		a='0'
	
	if b is None:
		b='0'

	# 参数一定默认是字符型，转换需要进行try
	try:
		a=int(a)
		b=int(b)
	except:
		a=0
		b=0
		
	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Title Here</title>
</head>
<body>

<h1>矩形面积的计算</h1>
<p>
<form method="get" action="/rectarea4.do">
长：<input type="text" name="a" value="{}">
宽：<input type="text" name="b" value="{}">
<br>
<input type="submit" value="计算面积">

</form>
</p>

<h1>计算得到的面积为：{}</h1>

</body>
</html>
	
	'''.format(a,b,a*b)
	
	return html

@app.route('/rectarea5.do',methods=['GET','POST'])
def rectangle_area5():
	print(request.method)
	if request.method == 'POST':
		a = request.form.get('a')
		b = request.form.get('b')
	else:
		a = request.args.get('a')
		b = request.args.get('b')
		
	if a is None:
		a='0'
	
	if b is None:
		b='0'

	# 参数一定默认是字符型，转换需要进行try
	try:
		a=int(a)
		b=int(b)
	except:
		a=0
		b=0
		
	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Title Here</title>
</head>
<body>

<h1>矩形面积的计算</h1>
<p>
<form method="post" action="/rectarea5.do">
长：<input type="text" name="a" value="{}">
宽：<input type="text" name="b" value="{}">
<br>
<input type="submit" value="计算面积">

</form>
</p>

<h1>计算得到的面积为：{}</h1>

</body>
</html>
	
	'''.format(a,b,a*b)
	
	return html
	
if __name__ == '__main__':
	app.run(debug=True)
	# print(read_excel_data())
		