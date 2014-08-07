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

##流程说明
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