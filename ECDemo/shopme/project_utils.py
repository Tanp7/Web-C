#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 项目的一些通过方法定义

import time
import json
import random
import os
from flask import make_response,jsonify

# 加密需要的模块
import hashlib
import base64

#接收字典及名称参数变成一个新的字典
def make_dict(*args,**kwargs):
	#返回的结果字典
	rst = {}
	#匿名参数的index
	anom_arg_idx = 0
	if len(args)>0:
		for item in args:
			if isinstance(item,dict):
				#如果匿名参数的类型为字典，则直接更新到返回字典钟
				rst.update(item)
			else:
				#如果匿名类型为一般类型，则建立新的字典熟悉，名称为：anom_arg_0
				rst['anom_arg_'+str(anom_arg_idx)] = item
				anom_arg_idx += 1
				
	if len(kwargs)>0:
		rst.update(kwargs)
	
	return rst
	
#产生json跨域的json返回
def to_json_cors(*args,**kwargs):
	rst = make_dict(*args,**kwargs)
	resp = make_response(json.dumps(rst))
	resp.headers['Content-Type'] = 'application/json'
	#跨域必须有的
	resp.headers['Access-Control-Allow-Origin'] = '*'
	#跨域可选的
	resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
	resp.headers['Access-Control-Allow-Credentials'] = 'true'
	resp.headers['Access-Control-Allow-Headers'] = 'Origin,X-Requested-With,Content-Type,Accept'
	
	return resp
	
#直接用jsonify返回一个json，只有本系统中可以用
def to_json(*args,**kwargs):
	return jsonify(make_dict(*args,**kwargs))
	
#字符形式的日期转成时间戳
def datestr_to_timestamp(datestr,**kwargs):
	#日期格式的默认值
	fmt = '%Y-%m-%d %H:%M:%S'
	if len(kwargs)>0 and ('format' in kwargs):
		fmt = kwargs['format']
	ts = int(time.mktime(time.strptime(datestr, fmt)))
	return ts

	
#时间戳转成日期字符串
def timestamp_to_datestr(timestamp,**kwargs):
	fmt = '%Y-%m-%d %H:%M:%S'
	if len(kwargs)>0 and ('format' in kwargs):
		fmt = kwargs['format']
	dt = time.strftime(fmt, time.localtime(timestamp))
	return dt
	
#获得当前的时间戳，单位秒
def now_timestamp():
	return (int)(time.time())
	
# 字符串的MD5加密，一般用于密码的保存
def md5_encode(plaintext):
	#加密的明文必须是字符串或者字节数组
	if type(plaintext)==type(''):
		data = plaintext.encode('utf-8')
	elif type(plaintext)==type(b''):
		data = plaintext
	else:
		return 'plaintext must be str or bytes'
		
	#获得md5算法对象
	md5 = hashlib.md5()
	#执行加密动作，明文需要首先转成字节数组才能进行加密
	md5.update(data)
	#以16进制字符形式得到加密后的字符串，称之为 密文
	return md5.hexdigest()
	
# base64 加密，加密对象为字节数组
def base64_encode(plaintext):
	#加密的明文必须是字符串或者字节数组
	if type(plaintext)==type(''):
		data = plaintext.encode('utf-8')
	elif type(plaintext)==type(b''):
		data = plaintext
	else:
		return 'plaintext must be str or bytes'
		
	data_base64 = base64.b64encode(data)
	return data_base64.decode('utf-8')
	
# base64 解密，解密对象必须是字符串或者字节数组
def base64_decode(ciphertext):
	if type(ciphertext)==type(''):
		data_base64 = ciphertext.encode('utf-8')
	elif type(ciphertext)==type(b''):
		data_base64 = ciphertext
	else:
		return 'ciphertext must be str or bytes'
		
	data = base64.b64decode(data_base64)
	return data.decode('utf-8')
	
# 产生验证码，4位，大写
def gnr_check_code():
	chars = '23456789abcdefghjkmnpqrstuvwxyz';
	lt = len(chars)
	# print(random.randint(0,lt))
	ls = []
	for i in range(4):
		ls.append(chars[random.randint(0,lt-1)])
		
	return ''.join(ls).upper()
	
# 获得项目的所在文件夹路径，作为其它资源的根目录
cur_project_path = None
def get_project_dir():
	# 申明使用外部的 cur_project_path
	global cur_project_path
	# 项目路径只需要获得一次即可
	if cur_project_path is not None:
		return cur_project_path
		
	cur_project_path = os.path.dirname(os.path.abspath(__file__))
	if cur_project_path.find('\\')!=-1:
		cur_project_path = cur_project_path.replace('\\','/')
	
	return cur_project_path
	
	
# 获得数据库db文件的路径
def get_db_path():
	return get_project_dir()+'/shopme.db'
	

#作为主模块时候的执行，一般测试函数使用
if __name__ == '__main__':
	# plaintext = '你好啊'
	# print('明文：',plaintext)
	
	# ciphertext = base64_encode(plaintext)
	# print('base64 加密：',ciphertext)
	# str = base64_decode(ciphertext)
	# print('base64 解密：',str)
	
	# print('md5 加密：',md5_encode(plaintext))
	
	
	print(gnr_check_code())
	
	
	
	
	