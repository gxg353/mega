# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:apis.task
'''
## to do 
# import MegaClient
from lib.logs import Logger

from mega_service.mega_client.sender import MegaClient



MODEL='API-task'
log=Logger(MODEL).log()


def remote_cmd(ip,port,cmd,target,args=None):
    '''
        ip port:instance info
        cmd :task name
        target: python,shell,cmd
    '''
    log.debug(args)
    c=MegaClient(host=ip,port=1105,cmd=cmd)
    result=c.run(func_args=args,TARGET=target)
    log.debug(result)
    return result