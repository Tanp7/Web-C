#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# Jinja2 的基本用法:   https://www.jianshu.com/p/f04dae701361
import os
from jinja2 import PackageLoader,FileSystemLoader,Environment

# 使用包加载器来加载
# env = Environment(loader=PackageLoader('shopeme','templates'))


#获得当前文件夹，绝对路径
cur_dir = os.path.dirname(os.path.abspath(__file__))
#如果存在windows中的\\路径字符，需要替换为 /
if cur_dir.find('\\')!=-1:
	cur_dir = cur_dir.replace('\\','/')
#模板所在的文件夹
template_dir = cur_dir+'/templates'

# 使用文件系统加载器来加载，指定搜索目录: searchpath=template_dir
env = Environment(loader=FileSystemLoader(searchpath=template_dir))

# 获得模板
tmpl = env.get_template('ztest_jinja2_1.html')

# 模板渲染，返回渲染后的字符串
str = tmpl.render(name='张十三')

print(str)

