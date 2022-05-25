#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 主蓝图，直接构建在 /
# 主要是前台网页使用的一些模块

#引入蓝图使用的模块
from flask import Blueprint,request,session,url_for,render_template
# 引入工具模块
import shopme.project_utils as pju

import sqlite3


# 创建主蓝图对象，一般命名为 main
main = Blueprint('main',__name__)


# 获得每日特价商品的列表
# 定义为函数，将cursor对象传递过来，这样不用多次打开数据库
def get_ls_dayspecial(cursor):
	#每日特价产品的列表，获得排序号最高的8个
	ls_dayspecial=[]
	sql = 'select t1.id,t1.proid,t1.seqno,t2.title,t2.priceold,t2.pricenew,t2.priceunit from tdayspecial t1,tproduct t2 where t1.proid=t2.id order by t1.seqno limit 8'
	
	result_all = cursor.execute(sql).fetchall()
	for line in result_all:
		record = {};
		record['id']=line[0]
		record['proid']=line[1]
		record['seqno']=line[2]
		record['title']=line[3]
		record['priceold']=line[4]
		record['pricenew']=line[5]
		record['priceunit']=line[6]
			
		record['pricesign']='￥'
		if record['priceunit']=='USD':
			record['pricesign']='$'
				
		ls_dayspecial.append(record)
		
	# 还需要去找这个商品的第一张 正常大小的图片，作为商品的默认图片
	for record in ls_dayspecial:
		sql = 'select imgnormal from tproimg where proid=? order by seqno limit 1'
		result_one = cursor.execute(sql,(record['proid'],)).fetchone()
		record['defaultimg'] = result_one[0] if (result_one is not None) else '/images/404.jpg'
		
	return ls_dayspecial
	
# 获得最新推荐的数据字典，要根据tabloc分类，每类是一个列表
def get_dt_newarrival(cursor):
	dt={}
	
	#找出 tnewarrival 表中所有不重复的tabloc
	sql = 'select distinct tabloc from tnewarrival'
	result_all = cursor.execute(sql).fetchall()
	for line in result_all:
		#每个 tabloc 作为字典的key，value是空列表
		dt[line[0]]=[]
		
	# 根据字典的每个key，再继续查询该分组下的商品，每组最多8个商品
	for key in dt.keys():
		sql = 'select t1.id,t1.proid,t1.seqno,t2.title,t2.priceold,t2.pricenew,t2.priceunit from tnewarrival t1,tproduct t2 where t1.proid=t2.id and t1.tabloc=? order by t1.seqno limit 8'
		result_all = cursor.execute(sql,(key,)).fetchall()
		for line in result_all:
			record = {}
			record['id']=line[0]
			record['proid']=line[1]
			record['seqno']=line[2]
			record['title']=line[3]
			record['priceold']=line[4]
			record['pricenew']=line[5]
			record['priceunit']=line[6]
				
			record['pricesign']='￥'
			if record['priceunit']=='USD':
				record['pricesign']='$'
					
			dt[key].append(record)
			
		for record in dt[key]:
			sql = 'select imgnormal from tproimg where proid=? order by seqno limit 1'
			result_one = cursor.execute(sql,(record['proid'],)).fetchone()
			record['defaultimg'] = result_one[0] if (result_one is not None) else '/images/404.jpg'
		
	return dt;

# route路由对象，可以设置方法：methods=['GET','POST']，不设置默认为GET
#定义网站的主页
@main.route('/',methods=['GET','POST'])
def index():

	# data_modal 对象，字典，表示要传递到页面去的数据内容
	data_modal = {}

	# 数据库中获取每日特价和最新推荐的信息，放置到相应的div中
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	
	
	#将每日特价的列表加入到数据模型中
	data_modal['dayspecial'] = get_ls_dayspecial(cursor)
	
	data_modal['newarrival'] = get_dt_newarrival(cursor);
	
	conn.close()

	return render_template('index.html',data_modal=data_modal)
	
# 获得商品的详情，简介和详情都需要用到
def get_product_info(id):
	# 根据id号获得商品简介模板: quick_view.html 需要的信息
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	sql = 'select id,code,title,manufacturer,brand,stock,markshort,markdetail,specification,size,priceold,pricenew,priceunit from tproduct where id=?'
	result_one = cursor.execute(sql,(id,)).fetchone()
	if result_one is None:
		conn.close()
		return render_template('modal_404.html',error='无法找到商品信息. id={}'.format(id))
		
	#定义商品对象，字典，作为返回给模板的数据
	data_modal = {}
	data_modal['id']=result_one[0]
	data_modal['code']=result_one[1]
	data_modal['title']=result_one[2]
	data_modal['manufacturer']=result_one[3]
	data_modal['brand']=result_one[4]
	data_modal['stock']=result_one[5]
	data_modal['markshort']=result_one[6]
	data_modal['markdetail']=result_one[7]
	data_modal['specification']=result_one[8]
	data_modal['size']=result_one[9]
	data_modal['priceold']=result_one[10]
	data_modal['pricenew']=result_one[11]
	data_modal['priceunit']=result_one[12]
	
	data_modal['pricesign']='￥'
	if data_modal['priceunit']=='USD':
		data_modal['pricesign']='$'
		
	# 把 size 按照逗号进行拆分，为数组
	data_modal['sizearray'] = data_modal['size'].split(',')
		
	# 获得该商品的全部图片，保存在列表中
	imgs = []
	sql = 'select imgnormal,imgthumb,imglarge from tproimg where proid=? order by seqno'
	result_all = cursor.execute(sql,(id,)).fetchall()
	for line in result_all:
		# 内容较少，可以快速一次性组装字典
		imgs.append({
			'imgnormal':line[0],
			'imgthumb':line[1],
			'imglarge':line[2]
		})
		
	#如果没有图片，放置一张404
	if len(imgs)==0 :
		imgs.append({
			'imgnormal':'/images/404_2.jpg',
			'imgthumb':'/images/404_2.jpg',
			'imglarge':'/images/404_2.jpg'
		})
		
	data_modal['imgs'] = imgs
	
	conn.close()
	
	return data_modal
	
# 商品简介
@main.route('/product_quickview.do',methods=['GET','POST'])
def product_quickview():
	# 获得商品的id号，区分post和get方式
	if request.method == 'POST':
		id = int(request.form['id']) if ('id' in request.form) else 0
	else:
		id = int(request.args['id']) if ('id' in request.args) else 0
		
	return render_template('quick_view.html',data_modal=get_product_info(id))
		
	
@main.route('/product_detail.do',methods=['GET','POST'])
def product_detail():
	if request.method == 'POST':
		id = int(request.form['id']) if ('id' in request.form) else 0
	else:
		id = int(request.args['id']) if ('id' in request.args) else 0

	return render_template('product_detail.html',hide_layerslider=True,data_modal=get_product_info(id))
	
@main.route('/orderlist.do',methods=['GET','POST'])
def orderlist():
	return render_template('orderlist.html')