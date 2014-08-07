# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_service.mega_client.worker
'''
import commands
import sys,os
import time

from setting import SCRIPT_DIR,DEFAULT_TARGET
from script import ping
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
        '''
            {'TARGET': 'python', 'ARGS': "{'ip': u'localhost', 'version': u'5.6', 'id': 12L, 'port': 3310L}", 
            'VALUE': 'test.py', 'TIME': 0, 'TYPE': 0, 'CYCLE': 0}
            TYPE:
                 0 call the script outside mega project:setting.SCRIPT_DIR
                 1 call the script in diretory :mega_client/script/
        '''
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
        _cmd_type=self.data.get('TARGET')
        _type=self.data.get('TYPE')
        if _type == '0':
            script_dir=SCRIPT_DIR
        else:
            script_dir=os.path.join(sys.path[0],'script/')
        if  _cmd_type== 'cmd':
            _cmd_type=''
        _cmd="%s %s%s \"%s\" " % (_cmd_type,script_dir,self.data['VALUE'],self.data['ARGS'])
        log.debug(_cmd)
        status,output=commands.getstatusoutput(_cmd)
        if status <>0:
            log.error(str(status)+' : '+output)
        return status,output
class Monitor():
    '''
        client monitor
    '''
    
    def __init__(self):
        self.sleep=30
    
    def monitor(self):
        log.info("Monitor is Starting...")
        _count=0  
        try:
            while 1:
                keepalive=ping.main()
                if keepalive == 'failed':
                    _count+=1
                    log.error('keepalive check :%s'% keepalive)
                if _count >100:
                    break
                    log.error('keepalive check  :%s for %s times ,abort!'% (keepalive,_count))
                time.sleep(self.sleep)
        except Exception as ex:
            log.error(ex)
        return