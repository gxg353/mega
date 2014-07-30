# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_service.mega_client.worker
'''
import commands

from setting import SCRIPT_DIR,DEFAULT_TARGET

from logs import Logger


MODEL='Worker'
log = Logger(MODEL).log()


class Worker():
    
    def __init__(self,cmd):
        self.cmd=cmd
        self.error=''
        self.error_code=0
        self.data={}
        
    def _work_resolve(self):
        _item=['TYPE','TIME','VALUE','CYCLE','TARGET','ARGS']
        _data={}
        self.cmd=eval(self.cmd)
        for i in _item:
            _data[i]=self.cmd.get(i,None)
        if not _data['VALUE']:
            return False
        if not _data['TARGET']:
            _data['TARGET']=DEFAULT_TARGET
        self.data=_data
        log.debug(self.data)
        return True
        
    def run(self):
        if not self._work_resolve():
            return self.error_code,self.error
        _type=self.data['TARGET'].upper()
        if  _type== 'cmd':
            _type=''
        _cmd="%s %s%s \"%s\" " % (_type,SCRIPT_DIR,self.data['VALUE'],self.data['ARGS'])
        log.debug(_cmd)
        status,output=commands.getstatusoutput(_cmd)
        log.debug(str(status)+output)
        return status,output