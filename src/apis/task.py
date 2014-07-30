# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:apis.task
'''

from lib.logs import Logger
try:
    from  mega_client.sender import MegaClient
except:
    from mega_client.mega_client.sender import MegaClient



MODEL='API-task'
log=Logger(MODEL).log()


def remote_cmd(ip,port,cmd,target,args=None):
    '''
        ip port:instance info
        cmd :task name or the script name
        target: python,shell,cmd
        args: for script
    '''
    log.debug(args)
    c=MegaClient(host=ip,port=1105,cmd=cmd)
    result=c.run(func_args=args,TARGET=target)
    log.debug(result)
    return result