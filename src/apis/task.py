# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:apis.task
'''

from lib.logs import Logger
from lib.PyMysql import PyMySQL
try:
    from  mega_client.sender import MegaClient
except:
    from mega_client.mega_client.sender import MegaClient


MODEL='API-task'
log=Logger(MODEL).log()


def remote_cmd(ip,port,cmd,cmd_type,task_id=None,args=None):
    '''
        ip port:instance info
        cmd :task name or the script name
        cmd_type: python,shell,cmd
        args: for script
    '''
    if task_id and args:
        args=str(task_id)+"  "+ args
    c=MegaClient(host=ip,port=1105,cmd=cmd)
    result=c.run(func_args=args,TARGET=cmd_type)
    log.debug("result for %s@%s:%s" %(cmd,ip,result))
    return result

def task_log(task_id,start_time,end_time,stat,redo=0,comment=''):
    value=(task_id,start_time,end_time,stat,redo,comment)
    sql="insert into task_log(task_id,start_time,end_time,stat,redo,comment) values(%s,'%s','%s',%s,%s,'%s')" % value
    log.debug(sql)
    result,ex=PyMySQL().execute(sql)
    if not result:
        log.error("Save task log failed as :%s" % ex)
        return (0,ex)
    return 1
    