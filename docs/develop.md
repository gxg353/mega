#开发规范

##目录说明
	
	mega/
		* api          公用调用接口
		* conf         配置文件
		* docs 		   各类文档
		* lib  		   公用库
		* log  		   日志
		* mega_server  服务后台
		* mega_web     web 项目
		* release      发布日志
		* scripts      脚本
		* tests		   测试用例

## 依赖包

python 2.6/2.7

Django-1.6.5

pip install django_chartit

python-daemon 1.5.5  <a>https://pypi.python.org/pypi/python-daemon/1.5.5]</a>

##代码规范

[google python stype](https://github.com/xchliu/zh-google-styleguide/blob/master/google-python-styleguide/python_style_rules.rst)

###字符集：utf8	# -*- coding: UTF-8 -*-


###定义

* 类命规则：单词首字母大写，无连接符，空2行，必须有`__init__`函数  class Daemon()
* 函数规则：小写，下划线连接，空1行，必须有`__doc__`   def mega_daemon(**argv)
* 内部函数：同函数，以下划线开头		def _run(self)


###函数：

* 显示定义参数格式及默认值
* 返回值必须为有效性，不能直接return，或return None

 
##api


##lib
* logs 日志统一模块
	
		MODEL='Listener'
		log = Logger(MODEL).log()
* PyMysql  连接MySQL通用库
* utils    常用小工具
* sendmail 邮件发送统一接口


###DB
数据库访问方式：

1. 使用models类 见mega_web/models/*

2. 使用MySQLdb  见lib/PyMysql


##mega_web
mega   主页

管理    资源管理

调度    任务调度管理

		
	url(r'^$',home),
    url(r'^resource/$',resource),
    url(r'^portal/$',portal),
    url(r'^monitor/$',monitor),
    url(r'console/$',console),
    url(r'charts/$',charts),
    url(r'^fun/$',fun),

	#sub url
    url(r'^resource/instance/$',instance),
    url(r'^resource/instance_add/$',instance_add),
    url(r'^resource/instance_detail/$',instance_detail),
    
    url(r'^resource/server/$',server),
    url(r'^resource/server_add/$',server_add),
    url(r'^resource/server_detail/$',server_detail),

    url(r'^resource/business/$',business),
    url(r'^resource/business_add/$',business_add),
    url(r'^resource/business_detail/$',business_detail),

    url(r'^resource/database/$',database),
    url(r'^resource/database_add/$',database_add),
    url(r'^resource/database_detail/$',database_detail),
    
    url(r'^resource/user/$',user),
    url(r'^resource/user_add/$',user_add),
    url(r'^resource/user_detail/$',user_detail),
    
    
    url(r'^console/backup/$',backup),
    url(r'^console/backup/backup_config/$',backup_config),
    url(r'^console/backup/backup_config_list/$',backup_config_list),

		
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
* init_db.sql  初始化项目db脚本
* install.sh   部署脚本
* mega_salt.py salt接口脚本
* mega_service.sh   mega服务脚本

##tests
路径:tests/*
####api
* api_resource.py  资源池管理接口测试用例
* slow_log.py   slow log添加接口
* update_backupinfo.py 备份过程中的信息更新接口
