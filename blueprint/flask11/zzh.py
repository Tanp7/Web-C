#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 蓝图模块

from flask import Blueprint,render_template

simple = Blueprint('simple',__name__)

@simple.route('/pz')
def f1():
	return "zzh"