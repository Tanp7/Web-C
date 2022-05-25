#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 蓝图，商品相关的操作，构建在：/product

from flask import Blueprint,request,session,url_for,render_template
import shopme.project_utils as pju
import sqlite3
import os

# 创建蓝图对象
product = Blueprint('product',__name__)

# 由于商品表的字段比较多，先整理到列表中，便于后续的数据获取
ls_fields = ['id','code','name','title','manufacturer','brand','stock','markshort','markdetail','specification','size','priceold','pricenew','priceunit','type1','type2','tags']

# 商品信息列表
@product.route('/',methods=['GET','POST'])
def index():
	login_admin = session.get('login_admin')
	
	if login_admin is None:
		return render_template('admin_login.html')
		
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
	# 组装sql语句
	# 因为需要根据条件组装where，所以使用 1=1 先写上 where 语法
	sql = 'select count(*) from tproduct where 1=1'
	# 在页面 type 中输入的值，涉及到: type1,type2,tags
	if type!='':
		sql += ' and (type1 like :type or type2 like :type or tags like :type)'
		dt_conn['type']='%'+type+'%'
	# 在页面 keyword 中输入的值，涉及到：name,title,brand,markshort
	if keyword!='':
		sql += ' and (name like :keyword or title like :keyword or brand like :keyword or markshort like :keyword)'
		dt_conn['keyword']='%'+keyword+'%'
	
	print('sql=',sql)
	
	result_one = cursor.execute(sql,dt_conn).fetchone()
	# 满足条件的记录总数
	total = result_one[0] if (result_one is not None) else 0
	data_modal['total']=total
	
	if total>0:
		# 当记录总数大于0的时候，继续查询本页数据
		sql = 'select '+(','.join(ls_fields))+' from tproduct where 1=1'
		if type!='':
			sql += ' and (type1 like :type or type2 like :type or tags like :type)'
			dt_conn['type']='%'+type+'%'
		if keyword!='':
			sql += ' and (name like :keyword or title like :keyword or brand like :keyword or markshort like :keyword)'
			dt_conn['keyword']='%'+keyword+'%'
		# 末尾加上排序和翻页语法
		sql += ' order by type1,type2'
		# sqlite数据库中的分页语法：limit 10 offset 0
		sql += ' limit '+str(pagesize)+' offset '+str((page-1)*pagesize)
		print('sql=',sql)
		
		# 返回查询的所有数据，组装 rows 对象，列表，内部字典
		rows = []
		result_all = cursor.execute(sql,dt_conn).fetchall()
		for line in result_all:
			record = {};
			# 根据字段列表中的顺序在加载数据到 record 字典中
			for i in range(len(ls_fields)):
				record[ls_fields[i]] = line[i]
				
			# 价格的符号
			record['pricesign']='￥'
			if record['priceunit']=='USD':
				record['pricesign']='$'
				
			rows.append(record)
			
		# 获得数据记录列表后，每行商品数据，还需要去获得所关联的图片数据
		for record in rows:
			# 每个商品有多个图片，列表存储
			imgs = []
			# 根据商品id查询图片，以 seqno 从小到大 升序排序
			sql = 'select id,proid,imgnormal,imgthumb,imglarge,seqno from tproimg where proid=? order by seqno'
			result_all = cursor.execute(sql,(record['id'],)).fetchall()
			# if result_all is not None:
			for line in result_all:
				img = {}
				img['id']=line[0]
				img['proid']=line[1]
				img['imgnormal']=line[2]
				img['imgthumb']=line[3]
				img['imglarge']=line[4]
				img['seqno']=line[5]
					
				imgs.append(img)
				
			# 将图片列表添加到商品记录中
			record['imgs']=imgs
			# 设置默认显示的图片，如果没有图片列表，则 404.jpg
			if len(imgs)==0:
				record['defaultimg']='/images/404.jpg'
			else:
				#使用第一张图片
				record['defaultimg']=imgs[0]['imgnormal']
			
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
		
	return render_template('admin_product_main.html',login_admin=login_admin,data_modal=data_modal)
	

# 新增或修改前，根据id号获得数据记录
@product.route('/presave.do',methods=['GET','POST'])
def presave():
	# 必须有id参数，表示数据库记录的id号，get和post或者参数的方式不一样，需要区分
	if request.method == 'POST':
		id = int(request.form['id']) if ('id' in request.form) else 0
	else:
		id = int(request.args['id']) if ('id' in request.args) else 0
		
	if id==0:
		#新增的情况，构造默认的 数据记录
		# 大部分字段都是 text，默认值为空字符串，先统一设置，再修改其中几项
		record = {};
		for i in range(len(ls_fields)):
			record[ls_fields[i]] = ''
			
		record['id']=0
		record['stock']=1
		record['priceold']=0.0
		record['pricenew']=0.0
		# 价格单位默认：CNY - 人民币
		record['priceunit']='CNY'
	else:
		#修改的情况，需要先根据id号去数据库中获得数据
		conn = sqlite3.connect(pju.get_db_path())
		cursor = conn.cursor()
		sql = 'select '+(','.join(ls_fields))+' from tproduct where id=?'
		result_one = cursor.execute(sql,(id,)).fetchone()
		if result_one is None:
			return pju.to_json(succ=False,stmt='无法找到记录. id={}'.format(id))
			
		# 根据字段顺序组装 record 字典
		record = {};
		for i in range(len(ls_fields)):
			record[ls_fields[i]] = result_one[i]
			
	#返回结果
	return pju.to_json(succ=True,record=record)
	
#tproduct 保存数据库
@product.route('/save.do',methods=['POST'])
def save():
	# 获得参数
	id = int(request.form['id'])
	code = request.form['code']
	name = request.form['name']
	title = request.form['title']
	manufacturer = request.form['manufacturer']
	brand = request.form['brand']
	stock = int(request.form['stock'])
	markshort = request.form['markshort']
	markdetail = request.form['markdetail']
	specification = request.form['specification']
	size = request.form['size']
	priceold = float(request.form['priceold'])
	pricenew = float(request.form['pricenew'])
	priceunit = request.form['priceunit']
	type1 = request.form['type1']
	type2 = request.form['type2']
	tags = request.form['tags']
	
	
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	# 判断code是否存在
	sql = 'select count(*) from tproduct where id<>? and code=?'
	result_one = cursor.execute(sql,(id,code)).fetchone()
	total = result_one[0] if (result_one is not None) else 0
	if total>0:
		# 已经存在，错误，注意，返回之前数据库链接必须断开
		conn.close()
		return pju.to_json(succ=False,stmt='商品编号已经存在. code={}'.format(code))
		
	# 根据id来判断是新增还是修改
	if id==0:
		# 新增，所需的字段为除去第一个id后面的那些字段
		ls_tmp = ls_fields[1:]
		sql = 'insert into tproduct('+(','.join(ls_tmp))+') values('
		# values 里面 ? 号的个数为：ls_tmp 的长度
		# 定义问好 ? 的列表
		ls_wh = []
		for i in range(len(ls_tmp)):
			ls_wh.append('?')
		# 将这些问好 ? 以逗号间隔字符串形式
		sql += ','.join(ls_wh)
		sql += ')'
		print('sql insert=',sql)
		
		# 按照顺序填充各个 ? 的值
		cursor.execute(sql,(code,name,title,manufacturer,brand,stock,markshort,markdetail,specification,size,priceold,pricenew,priceunit,type1,type2,tags))
	else:
		# 修改
		ls_tmp = ls_fields[1:]
		sql = 'update tproduct set '
		# set 后面的都是 code=?,name=? 先组装成列表，在形成字符串
		ls_wh = []
		for i in range(len(ls_tmp)):
			ls_wh.append(ls_tmp[i]+'=?')
		sql += ','.join(ls_wh)
		sql += ' where id=?'
		print('sql update=',sql)
		
		# 按照顺序填充各个 ? 的值，id放在最后面
		cursor.execute(sql,(code,name,title,manufacturer,brand,stock,markshort,markdetail,specification,size,priceold,pricenew,priceunit,type1,type2,tags,id))
		
	# insert 和 update 都改变了数据库记录，需要执行提交
	conn.commit()
	conn.close()
	
	#返回成功
	return pju.to_json(succ=True)
	

# 删除商品信息，如果商品有图片，也需要同时删除
@product.route('/delete.do',methods=['POST'])
def delete():
	# tproduct 表的 id
	id = int(request.form['id'])
	
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	# 首先删除 tproimg 表的信息和图片文件
	# 判断 tproimg 表中是否有本商品的图片
	sql = 'select count(*) from tproimg where proid=?'
	result_one = cursor.execute(sql,(id,)).fetchone()
	total = result_one[0] if (result_one is not None) else 0
	if total>0 :
		#存在商品的图片信息，查询出来，删除图片和数据库记录
		sql = 'select imgnormal,imgthumb,imglarge from tproimg where proid=?'
		result_all = cursor.execute(sql,(id,)).fetchall()
		for line in result_all:
			#获得三个图片的绝对路径，进行删除
			os.remove(pju.get_project_dir()+'/static'+line[0])
			os.remove(pju.get_project_dir()+'/static'+line[1])
			os.remove(pju.get_project_dir()+'/static'+line[2])
			
		# 删除数据库记录
		sql = 'delete from tproimg where proid=?'
		cursor.execute(sql,(id,))
		
	# 删除 每日特价 中该商品相关的记录
	sql = 'select count(*) from tdayspecial where proid=?'
	result_one = cursor.execute(sql,(id,)).fetchone()
	total = result_one[0] if (result_one is not None) else 0
	if total>0 :
		sql = 'delete from tdayspecial where proid=?'
		cursor.execute(sql,(id,))
		
	# 删除 新品推荐 中该商品相关的记录
	sql = 'select count(*) from tnewarrival where proid=?'
	result_one = cursor.execute(sql,(id,)).fetchone()
	total = result_one[0] if (result_one is not None) else 0
	if total>0 :
		sql = 'delete from tnewarrival where proid=?'
		cursor.execute(sql,(id,))
		
	# 删除商品信息记录
	sql = 'delete from tproduct where id=?'
	cursor.execute(sql,(id,))
	
	conn.commit()
	conn.close()
	
	return pju.to_json(succ=True)

# 图片上传参考: https://blog.csdn.net/qq_43317529/article/details/83096447
@product.route('/saveimg.do',methods=['POST'])
def saveimg():
	# 上传的商品图片的保存路径统一为：/static/uploads/proimages
	# 判断保存目录是否存在，不存在则要新建文件夹
	savedir = pju.get_project_dir()+'/static/uploads/proimages'
	if not os.path.exists(savedir):
		os.makedirs(savedir, 755)
		print('图片保存目录不存在，创建...')
		
	# 保存倒数据库中的 record 字典
	record = {}
		
	# 从表单对象中获得 proid 和 seqno 两个参数
	proid = int(request.form['proid'])
	seqno = int(request.form['seqno'])
	
	record['proid']=proid
	record['seqno']=seqno
	
	
	# 获得三个文件对象，使用新文件名，避免原文件名的复杂性
	# 当前时间戳，构造新文件名称使用
	nowtime = pju.now_timestamp()
	
	# =================正常图片=================
	f_imgnormal = request.files.get('imgnormal')
	if f_imgnormal is None:
		return pju.to_json(succ=False,stmt='无法获得文件对象: imgnormal')
	# 文件的原来名称
	filename = f_imgnormal.filename
	# 从原来名称中获得扩展名
	fileext = filename.split('.')[-1]
	# 组装新名称: imgnormal_proid_seqno_时间戳.扩展名
	newname = 'imgnormal_'+str(proid)+'_'+str(seqno)+'_'+str(nowtime)+'.'+fileext
	# 保存文件
	f_imgnormal.save(savedir+'/'+newname)
	#设置数据库中的图片路径
	record['imgnormal']='/uploads/proimages/'+newname
	
	
	# =================小图片=================
	f_imgthumb = request.files.get('imgthumb')
	if f_imgthumb is None:
		return pju.to_json(succ=False,stmt='无法获得文件对象: imgthumb')
	# 文件的原来名称
	filename = f_imgthumb.filename
	# 从原来名称中获得扩展名
	fileext = filename.split('.')[-1]
	# 组装新名称: imgnormal_proid_seqno_时间戳.扩展名
	newname = 'imgthumb_'+str(proid)+'_'+str(seqno)+'_'+str(nowtime)+'.'+fileext
	# 保存文件
	f_imgthumb.save(savedir+'/'+newname)
	#设置数据库中的图片路径
	record['imgthumb']='/uploads/proimages/'+newname
	
	
	# =================大图片=================
	f_imglarge = request.files.get('imglarge')
	if f_imglarge is None:
		return pju.to_json(succ=False,stmt='无法获得文件对象: imglarge')
	# 文件的原来名称
	filename = f_imglarge.filename
	# 从原来名称中获得扩展名
	fileext = filename.split('.')[-1]
	# 组装新名称: imgnormal_proid_seqno_时间戳.扩展名
	newname = 'imglarge_'+str(proid)+'_'+str(seqno)+'_'+str(nowtime)+'.'+fileext
	# 保存文件
	f_imglarge.save(savedir+'/'+newname)
	#设置数据库中的图片路径
	record['imglarge']='/uploads/proimages/'+newname
	
	# 保存数据库，每次图片都是新增
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	sql = 'insert into tproimg(proid,imgnormal,imgthumb,imglarge,seqno) values(?,?,?,?,?)'
	cursor.execute(sql,(record['proid'],record['imgnormal'],record['imgthumb'],record['imglarge'],record['seqno']))
	
	conn.commit()
	conn.close()
	
	
	#返回成功
	return pju.to_json(succ=True)
	
# 改变商品图片的排序号
@product.route('/setimgseqno.do',methods=['POST'])
def setimgseqno():
	# tproimg 表的 id
	id = int(request.form['id'])
	seqno = int(request.form['seqno'])
	
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	sql = 'update tproimg set seqno=? where id=?'
	cursor.execute(sql,(seqno,id))
	
	conn.commit()
	conn.close()
	
	return pju.to_json(succ=True)
	
# 删除商品图片
@product.route('/deleteimg.do',methods=['POST'])
def deleteimg():
	# tproimg 表的 id
	id = int(request.form['id'])
	
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	# 根据id号找出图片信息，需要删除对应的图片
	sql = 'select imgnormal,imgthumb,imglarge from tproimg where id=?'
	result_one = cursor.execute(sql,(id,)).fetchone()
	if result_one is None:
		conn.close()
		return pju.to_json(succ=False,stmt='无法找到图片信息. id={}'.format(id))
		
	#数据库中的图片路径为：/uploads/proimages/imgthumb_2_1_1580787139.jpg
	#获得三个图片的绝对路径，进行删除
	os.remove(pju.get_project_dir()+'/static'+result_one[0])
	os.remove(pju.get_project_dir()+'/static'+result_one[1])
	os.remove(pju.get_project_dir()+'/static'+result_one[2])
	
	#删除数据库中的记录
	sql = 'delete from tproimg where id=?'
	cursor.execute(sql,(id,))
	
	conn.commit()
	conn.close()
	
	return pju.to_json(succ=True)
	
# 加入 每日特价
@product.route('/add_dayspecial.do',methods=['POST'])
def add_dayspecial():
	proid = int(request.form['proid'])
	seqno = int(request.form['seqno'])
	
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	# 判断该商品是否已经在每日推荐中了
	sql = 'select count(*) from tdayspecial where proid=?'
	result_one = cursor.execute(sql,(proid,)).fetchone()
	total = result_one[0] if (result_one is not None) else 0
	
	if total>0 :
		conn.close()
		return pju.to_json(succ=False,stmt='该商品已经在每日特价中了')
		
	# 新增
	sql = 'insert into tdayspecial(proid,seqno) values(?,?)'
	cursor.execute(sql,(proid,seqno))

	conn.commit()
	conn.close()
	
	return pju.to_json(succ=True)
	
# 加入 新品推荐
@product.route('/add_newarrival.do',methods=['POST'])
def add_newarrival():
	proid = int(request.form['proid'])
	seqno = int(request.form['seqno'])
	tabloc = request.form['tabloc']
	
	# 如果没有填写 tabloc，则默认：tab-default
	if tabloc=='':
		tabloc = 'tab-default'
	
	conn = sqlite3.connect(pju.get_db_path())
	cursor = conn.cursor()
	
	# 判断该商品是否已经在新品推荐中了
	sql = 'select count(*) from tnewarrival where proid=?'
	result_one = cursor.execute(sql,(proid,)).fetchone()
	total = result_one[0] if (result_one is not None) else 0
	
	if total>0 :
		conn.close()
		return pju.to_json(succ=False,stmt='该商品已经在新品推荐中了')
		
	# 新增
	sql = 'insert into tnewarrival(proid,seqno,tabloc) values(?,?,?)'
	cursor.execute(sql,(proid,seqno,tabloc))

	conn.commit()
	conn.close()
	
	return pju.to_json(succ=True)
	
