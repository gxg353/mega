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
#record_id,module,re_time,time_used,result,content
for _cmd,f in cmd.iteritems():
    c=sender.MegaClient(host=MEGA_HOST,cmd=_cmd)
    r=c.run(func_args=f)
    c.close()    
    print "test %s %s: %s" %(_cmd,f,r)

