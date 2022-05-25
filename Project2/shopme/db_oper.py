#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   : iceking  2020-2-1

# 数据库操作模块，sqlite3数据库，数据库名称：shopme.db

import os
#引入 sqlite3模块，操作数据库
import sqlite3
# 引入工具模块
import shopme.project_utils as pju

#获得当前文件夹，绝对路径
cur_dir = os.path.dirname(os.path.abspath(__file__))
#如果存在windows中的\\路径字符，需要替换为 /
if cur_dir.find('\\')!=-1:
	cur_dir = cur_dir.replace('\\','/')
#数据库文件的路径
db_path = cur_dir+'/shopme.db'
print('数据库文件路径：'+db_path)


# 数据库初始化，加入 超级管理员 admin
def init_database():
	#打开数据库链接
	conn = sqlite3.connect(db_path)
	#获得数据库访问的游标
	cursor = conn.cursor()
	
	#查询表 tadmin 中是否有记录
	sql = '''
	select count(*) from tadmin
	'''
	
	result_one = cursor.execute(sql).fetchone()
	total = result_one[0]
	if total==0:
		# tadmin 表空，则加入超级管理员数据记录, 超管 type=9
		sql = '''
		insert into tadmin(code,name,username,password,type) 
		values(?,?,?,?,?)
		'''
		#问号的数据元组
		record_data = ('S0001','SuperAdmin','admin',pju.md5_encode('admin'),9)
		#执行
		cursor.execute(sql,record_data)
		#提交
		conn.commit()
		
		print('创建 超级管理员 ...')
	
	#关闭本次链接，必须
	conn.close()
	
# 根据用户名和密码获得管理员记录，登入验证使用
def admin_findByUP(username,password):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	
	sql = '''
	select id,code,name,username,type from tadmin 
	where username=? and password=?
	'''
	
	# 密码需要进行 md5的加密，才可以和数据库进行匹配
	result_one = cursor.execute(sql,(username,pju.md5_encode(password))).fetchone()
	if result_one is None:
		return None;
	
	# 获得的第一条记录，返回一个元组，需要按照顺序整理为字典
	record = {};
	record['id']=result_one[0]
	record['code']=result_one[1]
	record['name']=result_one[2]
	record['username']=result_one[3]
	record['type']=result_one[4]
	
	conn.close()
	return record
	
# 根据id号找到管理员记录
def admin_tadmin_findById(id):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	sql = 'select id,code,name,username,type from tadmin where id=?'
	result_one = cursor.execute(sql,(id,)).fetchone()
	if result_one is None:
		return None;
		
	record = {};
	record['id']=result_one[0]
	record['code']=result_one[1]
	record['name']=result_one[2]
	record['username']=result_one[3]
	record['type']=result_one[4]
	
	conn.close()
	return record
	
'''
产品表的结构定义：
========================================================
tproduct: 商品基本信息表

id: 主键，自增
code: 产品的编号
name: 产品名称
title: 产品标题
manufacturer: 制造厂商
brand: 商标 / 品牌
stock: 库存量
markshort: 简介
markdetail: 详细介绍，
			以 html: 开头: 内容写在另外的局部网页中，去获得网页的内容
			以 url:  开头：内容写在另外一个完整的网页中，需要使用iframe去加载
specification: 产品规格型号等参数
			以 html: 开头: 内容写在另外的局部网页中，去获得网页的内容
			以 url:  开头：内容写在另外一个完整的网页中，需要使用iframe去加载
size: 商品尺寸（大、中、小等），多个以英文逗号隔开
priceold: 商品的原价
pricenew: 商品的现价
priceunit: 价格的单位，人民币，美元等
type1: 一级分类
type2: 二级分类
tags: 商品的关键字标签，多个以英文逗号隔开

==============================================================
tproimg: 商品的图片表

id: 主键，自增
proid: 关联 tproduct.id 外键
imgnormal: 商品图片的路径，正常大小，一般建议为：360*360尺寸，首页中正常显示的图片
imgthumb: 商品的缩略图，小尺寸，一般为：80*80
imglarge: 商品大图，一般为：800*800
seqno: 图片的索引号，0开始，0表示第一张图片


=============================================================
tdayspecial:  主页上的每日特价商品模块，由商品记录推荐进去

id: 主键，自增
proid: 关联 tproduct.id 外键
seqno: 排序的索引号

=============================================================
tnewarrival:  主页上的最新推荐模块，由商品记录推荐进去

id: 主键，自增
proid: 关联 tproduct.id 外键
seqno: 排序的索引号
tabloc: 放置到哪个tab页中


===============表结构定义：==========================

CREATE TABLE "tadmin" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"code"	TEXT,
	"name"	TEXT,
	"username"	TEXT,
	"password"	TEXT,
	"type"	INTEGER
)

CREATE TABLE "tproduct" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"code"	TEXT,
	"name"	TEXT,
	"title"	TEXT,
	"manufacturer"	TEXT,
	"brand"	TEXT,
	"stock"	INTEGER,
	"markshort"	TEXT,
	"markdetail"	TEXT,
	"specification"	TEXT,
	"size"	TEXT,
	"priceold"	REAL,
	"pricenew"	REAL,
	"priceunit"	TEXT,
	"type1"	TEXT,
	"type2"	TEXT,
	"tags"	TEXT
)

CREATE TABLE "tproimg" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"proid"	INTEGER NOT NULL,
	"imgnormal"	TEXT,
	"imgthumb"	TEXT,
	"imglarge"	TEXT,
	"seqno"	INTEGER
)

CREATE TABLE "tdayspecial" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"proid"	INTEGER NOT NULL,
	"seqno"	INTEGER
)

CREATE TABLE "tnewarrival" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"proid"	INTEGER NOT NULL,
	"seqno"	INTEGER,
	"tabloc"	TEXT
)


================================================================


'''

