from resource import * 
from manage import *
from task import * 
from tools import * 
from report import *
from mega_web.console.failover import  FailoverManage
add_failover_record=FailoverManage(None).add_failover_record
add_failover_record_detail=FailoverManage(None).add_failover_record_detail
stat_failover_record=FailoverManage(None).stat_failover_record