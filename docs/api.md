#API 

##通用API

##资源池API
*	def get_all_instance(model=None,stat=0,count=0):
    
    return all instance object as a list of  dicts and an error code sign the result, 0 means success
    
    keys:
    	
    	id ip port server_id name  level stat business_id business owner_id owner db_type ha_type online_date
    
        
    model :the model who do the api calling
    
    stat:   
    
    		0 all  (default) 
            1 only the online instance 
            2 only the offline instances
 
    count: counts of instances for return ,default 0(all)
    
* def get_all_server(model=None,stat=0,count=0):
 
    return a list of dicts and an error code sign the result, 0 means success
    
    keys: 
    	
    	id,ip,name,os,stat,owner,owner_name,online_date
    
    model :the model who do the api calling
    
    stat: 
    	
    		0 all  (default)  
            1 only the online instance 
            2 only the offline instances
    
    
    count: counts of instances for return ,default 0(all)

* def get_all_db(model=None,stat=0,count=0):
  
    return a list of dicts and an error code sign the result, 0 means success
  
    keys: 
    
		id,ip,port,name,level,instance_id,business_id,business,owner,owner_nameo,nline_date,stat
     
    model :the model who do the api calling
  
    stat: 
    		
    		0 all  (default)  
            1 only the online instance 
            2 only the offline instances

    count: counts of instances for return ,default 0(all)    
* def get_instance(model=None,ip=None,port=3306):
  
    Return a dict of instance data and an error code 
  
    keys : 
    	
    	id ip port server_id stat name level db_type online_date business_id  owner ha_type
  
	model:the model who do the api calling
  
    ip : instance ip
  
    port: port(default 3306)
 
* def get_database(model=None,ip=None,port=3306,db=None):

    Return a dict of database data and an error code

    keys :
    
	    id name level online_date business_id instance_id owner  stat

    model:the model who do the api calling

    ip : instance ip

    port: port(default 3306)

    db :  name of database

* def get_server(model=None,ip=None):
  
    Return a dict of server data and an error code
  
    keys :
    
    	stat name  ip online_date owner os id
  
    model:the model who do the api calling
  
    ip : server ip

* def add_server(ip,**args):
  
    Return an error code for the result of server add. 0 means success
  
    ip : server ip 
  
    args: server base info ,if not given ,default value will be used
  
    keys:server_name,server_online,server_owner,server_os 
* def mod_server(ip,**args):
  
    Return an error code for the result of server modify. 0 means success
  
    ip : server ip 
  
    args: server base info 
  
    keys:
    	
    	server_name,server_online,server_owner,server_os 
 
* def del_server(ip):

    Return an error code for the result of server del. 0 means success

    ip : server ip 
 
* def add_instance(ip,port,**args):
  
    Return an error code for the result of instance add. 0 means success
  
    ip: instance ip 
  
    port: instance port
  
    args:
    	
    	instance_level  instance_name  instance_bussiness instance_online instance_owner instance_dbtype instance_hatype
    
    If the server does not exists ,a new server will be add automatic
* def mod_instance(ip,port,**args):

	Return an error code for the result of server modify. 0 means success

    ip: instance ip 

    port: instance port

    args:
    	
    	instance_level  instance_name  instance_bussiness instance_online instance_owner instance_dbtype instance_hatype
* def del_instance(ip,port):
  
    Return an error code for the result of instance del. 0 means success
  
    ip : server ip 
  
    port : instance port
* def add_database(db,ip,port,**args):
 
    Return an error code for the result of instance add. 0 means success
 
    ip : server ip 
 
    db: db name
 
    port: instance port
 
    args: server base info ,if not given ,default value will be used

    keys:
    
    	database_ip database_port database_name database_level database_owner database_business database_online

    if the instance does not exists ,a new instance will be add automatic
* def mod_database(ip,port,db,**args):
  
    Return an error code for the result of database modify. 0 means success
  
    ip : server ip 
  
    db: db name
  
    port: instance port
  
    args: database base info ,if not given ,default value will be used
    
    keys:
    
    	database_ip database_port database_name database_level database_owner database_business database_online
   
* def del_database(ip,port,db):

    Return an error code for the result of database del. 0 means success

    ip : server ip 

    port : instance port

    db: db name

* def failover(group_name,old_master,new_master,method,time):
    '''
        1.update the instance and failover table ,change the replication relationship
        2.save the switch log
    '''
## 高可用接口
###MySQL
####接口定义

* def update_ha_info(new_master,old_master):
    * new_master 新主库实例:	IP:PORT
    * old_master 原主库实例:	IP:PORT 
    
        	switch the role inside a ha group
	        master format:'1.1.1.1:3306' 
        
    	    return ：
        		True | False
      
* def add_failover_record(self,failover_id,method,old_master,new_master,failover_name=None):

	* failover_id 高可用ip，脚本调用传None
	* method   		切换方式
	* old_master  原主库实例
	* new_master  新主库实例
	* failover_name  高可用组名，脚本调用传组名称
	
	        1.add a failover record with a given failover id  --used for mega web site
            2.add record with a failover group name  --used for command line ha switch
            
            return :
                None: failed to get the new record
                id(int): the new record for failover switch
* def add_failover_record_detail(self,record_id,module,re_time,time_used,result,content):
	* record_id  任务号，由函数add_failover_record（）返回或者mega 调用时提供
	* module     执行模块，
	* re_time 	 任务阶段记录时间
	* time_used  耗时
	* result 	 本阶段执行结果
	* content  	 执行信息
	
		    record_id  ,get from the function add_failover_record()
            1.if task invoked by mega, the id will be given
            2.if task begins from the command line, call the add_failover_record() and get the new record id befor add new detail logs
           
            return ：
				True | False

 
* def stat_failover_record(self,record_id,stat='Y'):
	* record_id  任务号
	* stat  执行结果，成功或者失败
		
			1.stat the result for a switch task
			
			return ：
				True | False

####测试用例

		import time
		from mega_client import sender
		from mega_client.setting import MEGA_HOST
		format='%Y-%m-%d %X'
		now=time.strftime(format, time.localtime())

		cmd={"update_ha_info":"'1.1.1.112:23','1.1.1.111:3306'",
		     #"add_failover_record":"10,'ONLINE','1.1.1.112:23','1.1.1.111:3306'",
		     "add_failover_record":"None,'ONLINE','1.1.1.112:23','1.1.1.111:3306','jjjj'",
		     "stat_failover_record":"32,'Y'",
		     "add_failover_record_detail":"31,'mega','%s','10','y','test the api'" % now,
     		}
		for _cmd,f in cmd.iteritems():
		    c=sender.MegaClient(host=MEGA_HOST,cmd=_cmd)
		    r=c.run(func_args=f)
		    c.close()    
		    print "test %s %s: %s" %(_cmd,f,r)

运行效果：
	
		xchliu@xchliu tests]$ python console_failover.py
		test add_failover_record None,'ONLINE','1.1.1.112:23','1.1.1.111:3306','jjjj': 32
		test add_failover_record_detail 31,'mega','2014-10-14 14:05:25','10','y','test the api': True
		test update_ha_info '1.1.1.112:23','1.1.1.111:3306': False
		test stat_failover_record 32,'Y': True
