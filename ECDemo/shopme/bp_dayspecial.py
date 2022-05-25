#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 蓝图，每日特价，构建在：/dayspecial

from flask import Blueprint,request,session,url_for,render_template
import shopme.project_utils as pju
import sqlite3

# 创建蓝图对象
dayspecial = Blueprint('dayspecial',__name__)

# 每日特价列表
@dayspecial.route('/',methods=['GET','POST'])
def index():
	# 接受查询相关几个参数，必须是post过来的
	if request.method == 'POST':
		type = request.form['type']
		keyword = request.form['keyword']
		page = int(request.form['page'])
		pagesize = int(request.form['pagesize'])
	else:
		# 默认情况，几个查询参数赋初始值
		type=''
		keyword=''
		page=1
		pagesize=10
		
	# data_modal 对象，字典，表示要传递到页面去的数据内容
	data_modal = {}
	# 从页面传递过来的几个参数也需要带回去，用于页面查询条件的填充
	data_modal['type']=type
	data_modal['keyword']=keyword
	data_modal['page']=page
	data_modal['pagesize']=pagesize
	
	#首先查询总的数量，直接使用数据库链接查询
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	# dt_conn 用来存放 sql 中的占位符数据，字典
	dt_conn = {}
	# 组装sql语句，由于type和keyword的内容是在 tproduct 表中的
	# 因此需要 tproduct 和 tdayspecial 两张表联合查询
	sql = 'select count(*) from tdayspecial t1,tproduct t2 where t1.proid=t2.id'
	# 在页面 type 中输入的值，涉及到: type1,type2,tags
	if type!='':
		sql += ' and (t2.type1 like :type or t2.type2 like :type or t2.tags like :type)'
		dt_conn['type']='%'+type+'%'
	# 在页面 keyword 中输入的值，涉及到：name,title,brand,markshort
	if keyword!='':
		sql += ' and (t2.name like :keyword or t2.title like :keyword or t2.brand like :keyword or t2.markshort like :keyword)'
		dt_conn['keyword']='%'+keyword+'%'
	
	print('sql=',sql)
	
	result_one = cursor.execute(sql,dt_conn).fetchone()
	# 满足条件的记录总数
	total = result_one[0] if (result_one is not None) else 0
	data_modal['total']=total
	
	if total>0:
		#查询本页数据，双表联合查询，只查询需要显示的几个即可
		sql = 'select t1.id,t1.proid,t1.seqno,t2.code,t2.name,t2.priceold,t2.pricenew,t2.priceunit from tdayspecial t1,tproduct t2 where t1.proid=t2.id'
		if type!='':
			sql += ' and (t2.type1 like :type or t2.type2 like :type or t2.tags like :type)'
			dt_conn['type']='%'+type+'%'
		if keyword!='':
			sql += ' and (t2.name like :keyword or t2.title like :keyword or t2.brand like :keyword or t2.markshort like :keyword)'
			dt_conn['keyword']='%'+keyword+'%'
		sql += ' order by t1.seqno'
		sql += ' limit '+str(pagesize)+' offset '+str((page-1)*pagesize)
		print('sql=',sql)
		
		rows = []
		result_all = cursor.execute(sql,dt_conn).fetchall()
		for line in result_all:
			record = {};
			record['id']=line[0]
			record['proid']=line[1]
			record['seqno']=line[2]
			record['code']=line[3]
			record['name']=line[4]
			record['priceold']=line[5]
			record['pricenew']=line[6]
			record['priceunit']=line[7]
			
			record['pricesign']='￥'
			if record['priceunit']=='USD':
				record['pricesign']='$'
				
			rows.append(record)
			
		# 还需要去找这个商品的第一张 正常大小的图片，作为商品的默认图片
		for record in rows:
			sql = 'select imgnormal from tproimg where proid=? order by seqno limit 1'
			result_one = cursor.execute(sql,(record['proid'],)).fetchone()
			record['defaultimg'] = result_one[0] if (result_one is not None) else '/images/404.jpg'
			
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
		
	return render_template('admin_dayspecial_main.html',login_admin='',data_modal=data_modal)
		
# 删除记录
@dayspecial.route('/delete.do',methods=['POST'])
def delete():
	id = int(request.form['id'])
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	sql = 'delete from tdayspecial where id=?'
	cursor.execute(sql,(id,))
	conn.commit()
	conn.close()
	return pju.to_json(succ=True)
	
# 调整排序号
@dayspecial.route('/setseqno.do',methods=['POST'])
def setseqno():
	id = int(request.form['id'])
	seqno = int(request.form['seqno'])
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	sql = 'update tdayspecial set seqno=? where id=?'
	cursor.execute(sql,(seqno,id))
	conn.commit()
	conn.close()
	return pju.to_json(succ=True)
	
# 调整价格，修改 商品表 tproduct
@dayspecial.route('/setprice.do',methods=['POST'])
def setprice():
	proid = int(request.form['proid'])
	priceold = float(request.form['priceold'])
	pricenew = float(request.form['pricenew'])
	
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	sql = 'update tproduct set priceold=?,pricenew=? where id=?'
	cursor.execute(sql,(priceold,pricenew,proid))
	conn.commit()
	conn.close()
	return pju.to_json(succ=True)
		
		
		