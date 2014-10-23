#wy python 公用库

##功能点

### 数据库连接
	* conn mysql 连接
### 邮件发送
	* sendmail  
	
### mega client
	
* logs	mega 客户端日志，调用后日志可打入client日志：/var/log/mega/mega_client.log
* sender mega 交互类，可调用服务端提供的api接口
* utils  工具类，包含各种通用性工具


##开发规范
	* 统一开发规范
	* 接口调用规范
###接口函数
获取mega service 支持的接口函数列表，使用下面的代码：
	
	>>> from mega_client import sender
	>>> c=sender.MegaTool()
	>>> c.get_all_funcs()

安全考虑，上面的代码只能在mega service 所在服务器可获取有效列表，其他节点返回列表为空。

>输出内容格式：

>* 接口函数名称，用于后续调用指定

>* 参数定义：

>	* args 为定义参数

>	* varargs 不定无名参数，即存在定义参数*args

>	* keywords	不定有名参数，即存在定义参数**kwargs
>   * defaults  默认值，tuple形式，对应args中每一个参数的默认值，None为无默认值

目前支持的接口参数：

update:2014-10-10

1. add_database ArgSpec(args=['ip', 'port', 'db'], varargs=None, keywords='args', defaults=None)
2. add_instance ArgSpec(args=['ip', 'port'], varargs=None, keywords='args', defaults=None)
3. add_server ArgSpec(args=['ip'], varargs=None, keywords='args', defaults=None)
4. add_slow_log ArgSpec(args=['log_info'], varargs=None, keywords=None, defaults=None)
5. backup_routine ArgSpec(args=['time'], varargs=None, keywords='args', defaults=(None,))
6. client_ping ArgSpec(args=['ip', 'version'], varargs=None, keywords='args', defaults=(None,))
7. client_upgrade ArgSpec(args=['host_list'], varargs=None, keywords=None, defaults=(None,))
8. del_database ArgSpec(args=['ip', 'port', 'db'], varargs=None, keywords=None, defaults=None)
9. del_instance ArgSpec(args=['ip', 'port'], varargs=None, keywords=None, defaults=None)
10. del_server ArgSpec(args=['ip'], varargs=None, keywords=None, defaults=None)
11. failover ArgSpec(args=['group_name', 'old_master', 'new_master', 'method', 'time'], varargs=None, keywords=None, defaults=None)
12. get_all_backup ArgSpec(args=[], varargs=None, keywords=None, defaults=None)
13. get_all_db ArgSpec(args=['model', 'stat', 'count'], varargs=None, keywords=None, defaults=(None, 0, 0))
14. get_all_instance ArgSpec(args=['model', 'stat', 'count', 'role'], varargs=None, keywords=None, defaults=(None, 0, 0, None))
15. get_all_server ArgSpec(args=['model', 'stat', 'count'], varargs=None, keywords=None, defaults=(None, 0, 0))
16. get_database ArgSpec(args=['model', 'ip', 'port', 'db'], varargs=None, keywords=None, defaults=(None, None, 3306, None))
17. get_instance ArgSpec(args=['model', 'ip', 'port'], varargs=None, keywords=None, defaults=(None, None, 3306))
18. get_server ArgSpec(args=['model', 'ip'], varargs=None, keywords=None, defaults=(None, None))
19. main ArgSpec(args=[], varargs=None, keywords=None, defaults=None)
20. mod_database ArgSpec(args=['ip', 'port', 'db'], varargs=None, keywords='args', defaults=None)
21. mod_instance ArgSpec(args=['ip', 'port'], varargs=None, keywords='args', defaults=None)
22. mod_server ArgSpec(args=['ip'], varargs=None, keywords='args', defaults=None)
23. remote_cmd ArgSpec(args=['ip', 'port', 'cmd', 'cmd_type', 'task_id', 'args'], varargs=None, keywords=None, defaults=(None, None))
24. report_routine ArgSpec(args=['time'], varargs=None, keywords=None, defaults=(None,))
25. slowlog_pack ArgSpec(args=['sql'], varargs=None, keywords=None, defaults=None)
26. slowlog_routine ArgSpec(args=['time'], varargs=None, keywords=None, defaults=(None,))
27. slowlog_statics ArgSpec(args=['time'], varargs=None, keywords=None, defaults=(None,))
28. slowlog_statics_per_hour ArgSpec(args=['v_time'], varargs=None, keywords=None, defaults=None)
29. task_log ArgSpec(args=['task_id', 'start_time', 'end_time', 'stat', 'redo', 'comment'], varargs=None, keywords=None, defaults=(0, ''))
30. update_backupinfo ArgSpec(args=['task_info', 'action'], varargs=None, keywords=None, defaults=('INSERT',))

###模块调用：

mega client 在安装或者升级时会将公用库放到该环境的python site package 中，使用时直接import 即可。 提供的公用库：

* sender
* logs
* setting
* utils
	* sendmail
	* get_ip_address

####sender
sender 为客户端与服务端核心交互模块，负责所有的数据发送。其中包含2个类：

* MegaClient  mega 客户端发送类，负责对数据包的检查，封装，与服务端的通信，数据包的拆包等操作
* MegaTool	   管理类，目前只包含一个函数，就是上面获取所有接口函数的函数

#####MegaClient
其中有2个常量：
  
	HOST = 'localhost'
	PORT = 1104
默认情况下，sender会向本地1104端口发送请求数据，因此在其他节点获取所有接口函数列表或者其他操作都会连接失败，返回空列表。可以通过加上HOST参数来解决：

	>>> from mega_client import sender
	>>> from mega_client.setting import MEGA_HOST
	>>> cmd='get_all_instance'
	>>> c=sender.MegaClient(host=MEGA_HOST,cmd=cmd)
	>>> c.run(func_args="model='backup',stat=1,role=1",CYCLE=1)
	>>> c.close()
**MegaClient.run** 参数说明

这里存在2层调用处理：

1. 当前代码对MegaClient类的调用
2. 在服务端对指定函数（cmd定义的函数名称）的调用

所以`run`函数需要处理自己的参数，也要接收目标函数的参数。函数的定义:

	def run(self,func_args=None,**args):  
* func_args 就是目标函数的调用参数，比如上面的func_args="model='backup',stat=1,role=1"，这些其实会传递给服务端的接口函数get_all_instance。
* **args 为run函数自己的运行参数，将作为客户端节点发送到服务端数据包的属性，目前会被解析的参数：

		_item=['TYPE','TIME','VALUE','CYCLE','TARGET','ARGS']
	 keys:
        *   TYPE:    0 internal server task,1 remote task
        *   VALUE:   func name which be called
        *   TIME:    when to do : 0 once  , relay to the CYCLE
            CYCLE:   lifecycle of job   day,week,month
            TARGET:  unique identify for server or instance or database.  
                     unique command type when in the case used for remote command etc.
                           *cmd
                           *python
                           *bash
            ARGS:    args for the api func
            TOOL:    Internal func calls
一般情况下，使用正常调用即可，不需要指定上面的参数，列出来是为了避免指定同名参数造成异常。以及一些确实需要改变请求动作的特殊情况。

**返回结果**

如果有返回结果，run函数会直接返回，返回内容为UTF8 编码的字符串，但格式一般都已经处理为list，对结果做eval()处理后即
可使用，不在sender完成对象转换有2个考虑：

1. 多语言调用，后续可实现通过命令行进行接口调用
2. 避免数据丢失

####logs
提供一个简单的日志类，能满足一般的日志需求。如果涉及handler ，level，切分等自定义，还是建议调用logging库来实现。

调用实例：	

	>>> import mega_client.logs
	>>> log=logs.Logger('test').log()
	>>> log.info('test')
其中Logger在初始化的时候如果参数logfile=None被赋值，返回的log对象会将日志打到指定文件中。

默认情况下，level为DEBUG，输出路径为/var/log/mega/mega_client.log,日志格式为一般通用日志格式。
####setting

客户端的配置文件放到公用库的目的是提供部分全局信息：

	CLIENT_DIR = '/home/mysql/'
    DAEMON_LOG = '/var/log/mega/mega_client.log'
    DAEMON_PID = '/var/run/mega_client.pid'
    DEAFULT_LOG_DEBUG = True
    DEFAULT_TARGET = 'cmd'
    KEEPALIVE = 300
    LOG_FILE_NAME = '/var/log/mega/mega_client.log'
    MEGA_HOST = '172.17.62.37'
    SCRIPT_DIR = '/home/mysql/admin/mega_client/script/'
    SERVICE_PID = '/var/run/mega_client_srv.pid'
    TCP_HOST = ''
    TCP_PORT = 1105
    version = 'mega-client 0.1'			

后续将实现客户端去服务器读取配置，如keepalived 监测周期，版本信息，访问本地数据库的账号密码等。

####utils

get_ip_address()获取本地hostname及ip地址。


##维护相关
###客户端安装

初始化客户流程：

* 拷贝客户端安装包到目标服务器：/home/xdba/
* root执行安装脚本：

		sudo bash install.sh 
客户端代码层级：
	
		.
		├── PKG-INFO
		├── build
		│   └── lib
		│       └── mega_client
		│           ├── __init__.py
		│           ├── client_main.py
		│           ├── listener.py
		│           ├── logs.py
		│           ├── mega_client.py
		│           ├── sender.py
		│           ├── setting.py
		│           ├── setup.py
		│           ├── utils.py
		│           └── worker.py
		├── install.sh
		├── mega_client
		│   ├── __init__.py
		│   ├── client_main.py
		│   ├── listener.py
		│   ├── logs.py
		│   ├── mega_client.py
		│   ├── sender.py
		│   ├── setting.py
		│   ├── setup.py
		│   ├── utils.py
		│   └── worker.py
		└── setup.py

###客户端升级

客户端实现自动化升级，完成代码迭代。

升级脚本：/mega_client/script/upgrade.py

* 升级发起方式
	* mega服务端任务推送
	* mega客户端发起请求
	
* 升级流程	
	* 服务端：在目录/mega/mega_client/中执行命令产生最新client 安装包：
	
			python setup.py sdist
			tar zxvf dist/mega-1.0.tar.gz

	* 客户端：完成本地环境检查和升级准备工作：upgrade.py:Upgrade._get_pag()
		
	* 客户端：调用本地client 中sender 模块，向服务器发送升级请求：
			
		    self.cmd='client_upgrade'
       		self.c=MegaClient(host='172.17.62.37',cmd=self.cmd)
			pag=self.c.run(func_args=ip,TOOL=True)
	* 服务端：解析数据包后，调用api中接口：

			2014-07-31 14:13:07 API-tool     DEBUG Receive upgrade request: ['192.168.199.245']
			2014-07-31 14:13:07 Worker       DEBUG Call API: apis.client_upgrade(['192.168.199.245'])
		
	* 服务端：在目录/mega_client/dist/中获取代码包，遍历目录文件，返回包含所有代码数据的[]
				  
			_pag.extend(read_file(_prefix,_prefix))
        	return _pag
	* 客户端：
		* 接收返回数据，还原代码包到临时目录：/tmp/
		* python package安装：
				
				python /tmpdir/setup.py install
		* 代码包替换,将本地服务包运行包替换为新代码包，默认本地服务运行路径：/home/xdba/

				cp -ar tmpdir clientdir
		* 重启client 服务：
					
				python /etc/init.d/mega_client restart	
* 操作流程
	* 确认服务端/mega_client/dist/ 目录有存在有效代码包：
		
			[xchliu@xchliu dist]$ ls
			mega-1.0        mega-1.0.tar.gz
	* 调度升级 
		* 服务器端配置调度任务，进行客户端升级

			<a href="http://172.17.61.63:8080/admin/client">mega任务调度</a>
		* 客户端运行升级脚本，进行单点升级：

				python upgrade.py