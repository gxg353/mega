#Mega 运维手册

##Mega Web 
* 启动
	
		uwsgi --yaml /export/servers/app/mega/src/wsgi.yaml
	
* 配置文件：

		$cat wsgi.yaml
		uwsgi:
			http: 0.0.0.0:8080
	 		chdir: /export/servers/app/mega/src
 			module: django_wsgi
 			processes: 2
	 		daemonize: /tmp/uwsgi.log
 			pidfile: /tmp/uwsgi.pid

* 正常启动日志：
		
		*** Starting uWSGI 2.0.7 (64bit) on [Mon Sep 22 17:49:17 2014] ***
		compiled with version: 4.4.7 20120313 (Red Hat 4.4.7-3) on 22 September 2014 16:19:56
		os: Linux-2.6.32-358.el6.x86_64 #1 SMP Fri Feb 22 00:31:26 UTC 2013
		nodename: MYSQL-YZH-6237
		machine: x86_64
		clock source: unix
		detected number of CPU cores: 24
		current working directory: /export/servers/app/mega/src
		writing pidfile to /tmp/uwsgi.pid
		detected binary path: /usr/bin/uwsgi
		!!! no internal routing support, rebuild with pcre support !!!
		*** WARNING: you are running uWSGI without its master process manager ***
		your processes number limit is 64000
		your memory page size is 4096 bytes
		detected max file descriptor number: 65535
		lock engine: pthread robust mutexes
		thunder lock: disabled (you can enable it with --thunder-lock)
		uWSGI http bound on 0.0.0.0:8080 fd 4
		spawned uWSGI http 1 (pid: 28736)
		uwsgi socket 0 bound to TCP address 127.0.0.1:17925 (port auto-assigned) fd 3
		Python version: 2.6.6 (r266:84292, Feb 22 2013, 00:00:18)  [GCC 4.4.7 20120313 (Red Hat 		4.4.7-3)]
		*** Python threads support is disabled. You can enable it with --enable-threads ***
		Python main interpreter initialized at 0x2677bf0
		your server socket listen backlog is limited to 100 connections
		your mercy for graceful operations on workers is 60 seconds
		mapped 145536 bytes (142 KB) for 2 cores
		*** Operational MODE: preforking ***
		WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x2677bf0 pid: 28735 		(default app)
		*** uWSGI is running in multiple interpreter mode ***
		spawned uWSGI worker 1 (pid: 28735, cores: 1)
		spawned uWSGI worker 2 (pid: 28737, cores: 1)
* 运行状态

		线程状态：
		[3-MySQL-Inst@MYSQL-YZH-6237 ~]
		$ps aux |grep wsgi
		xdba     28735  0.0  0.0 314472 27380 ?        S    17:49   0:00 uwsgi --yaml /export/servers/app/mega/src/wsgi.yaml
		xdba     28736  0.0  0.0  51420  1744 ?        S    17:49   0:00 uwsgi --yaml /export/servers/app/mega/src/wsgi.yaml
		xdba     28737  0.0  0.0 314576 26300 ?        S    17:49   0:00 uwsgi --yaml /export/servers/app/mega/src/wsgi.yaml
		xdba     33624  0.0  0.0 143720  4032 pts/16   S+   18:01   0:00 vim uwsgi.log
		root     35483  0.0  0.0 103244   852 pts/5    S+   18:06   0:00 grep wsgi

		网络监听：
		[3-MySQL-Inst@MYSQL-YZH-6237 ~]
		$netstat -lnpt |grep 8080
		tcp        0      0 0.0.0.0:8080                0.0.0.0:*                   LISTEN      28735/uwsgi
		
* 关闭
  
	  uwsgi --stop /tmp/uwsgi.pid
  执行后检查进程状态，确认关闭。
* 重启
  关闭后启动

