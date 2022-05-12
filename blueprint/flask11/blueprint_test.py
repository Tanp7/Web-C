#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 蓝图模块

from flask import Blueprint,render_template

t1 = Blueprint('t1',__name__)

@t1.route('/test', methods=['GET', 'POST'])
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