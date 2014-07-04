#开发规范

##目录说明
* api  公用调用接口
* docs 各类文档
* lib  公用库
* mega_web  网站项目
* scripts   脚本
* tests		测试代码及文档

##  依赖包
python 2.6/2.7

Django-1.6.5
pip install django_chartit

python-daemon 1.5.5  <a>https://pypi.python.org/pypi/python-daemon/1.5.5]</a>

##代码规范

* 字符集：utf8	# -*- coding: UTF-8 -*-


###定义

* 类命规则：单词首字母大写，无连接符，空2行，必须有`__init__`函数  class Daemon()
* 函数规则：小写，下划线连接，空1行，必须有`__doc__`   def mega_daemon(**argv)
* 内部函数：同函数，以下划线开头		def _run(self)

###参数：
*
###返回值
 
##api
接口规范
##docs
##lib
###DB
数据库访问方式：

1.使用models类 见mega_web/models/*

2.使用MySQLdb  见lib/PyMysql

##mega_web
mega   主页

管理    资源管理

调度
##mega_service
TCP 通信数据包规范：

        """        work instance:{'HEAD':'MEGA','TYPE':'CMD','VALUE':'ls'}
        keys:
            HEAD:    for safe interactive,should be MEGA
            TYPE:    cmd,task,other
            VALUE:   what to do : ls
            TIME:    when to do : 0 once  ,
            REPEAT:  lifecycle of job   day,week,month
            TARGET:    uniqeu identify for server or instance or database.
        """


##scripts
##tests
路径:tests/*
####api
* api_resource.py  资源池管理接口测试用例

  