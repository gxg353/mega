# -*- coding: UTF-8 -*-
'''
Created on Jul 1, 2014

@author: xchliu

'''

import socket
import types
import sys, os
app_path=os.path.dirname(sys.path[0])
sys.path.append(app_path)

from logs import Logger


MODEL='Sender'
log = Logger(MODEL).log()


TCP_HEADER={'HEAD':'MEGA'}
END_SIGN='eof'.upper()
BUFFER_SIZE=10
DEFAULT_NONE=0
HEADER_LENGTH=10


class MegaClient():
    '''
        Client for mega servcie .
        return a list d:
            * if all runs success ,the list contain all the data required
            * else only a 0 in the list means something goes into failure
        code example: 
            cmd='get_all_instance'
                c=MegaClient(cmd=cmd)
                if c:
                    data=c.run(func_args="model='backup',stat=1,role=1",CYCLE=1)
                    c.close()
                    return data
    '''
    HOST='localhost'
    PORT=1104
    def __init__(self,host=HOST,port=PORT,cmd=''):
        self._cmd={}
        self.host=host
        self.port=port
        socket.setdefaulttimeout(10)
        if cmd:
            self._cmd['VALUE']=str(cmd)
    
    def run(self,func_args=None,**args):
        if not self._cmd:
            return False
        _d=[]
        if self.conn():
            if func_args:
                self._cmd['ARGS']=str(func_args)
            if len(args)>0:
                self._cmd=dict(self._cmd,**args)            
            _d.append(1)
            _d.append(self.cmd_run(self._cmd))
        else:
            _d.append(0)
        if _d[0] == 1:
            return _d[1]
        else:
            return _d[0]
    
    def conn(self):
        try:       
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      
            self.s.connect((self.host,self.port))
            return True
        except Exception as ex:
            log.error("Connect to host : %s failed! %s" % (self.host,ex))
            return False
    
    def cmd_run(self,cmd=None):
        if not cmd:
            return False
        data=''
        _header=''
        try:
            cmd_with_pack=self._cmd_pack(cmd)
            if cmd_with_pack:
                _len=len(str(cmd_with_pack))+HEADER_LENGTH
                _header=str(_len)
                for i in range(HEADER_LENGTH - len(str(_len))):
                    _header='0'+_header
                self.s.sendall(_header+str(cmd_with_pack)+END_SIGN)
                header=int(self.s.recv(HEADER_LENGTH))
                while header>0:
                    _d=self.s.recv(BUFFER_SIZE)
                    data+=_d
                    if _d.find(END_SIGN) > 0:
                        break
                    header=header-HEADER_LENGTH
            return self._data_unpack(data)
        except Exception as ex:
            log.error(ex)
            return ''
    
    def _cmd_pack(self,data):
        '''
        keys:
        *   TYPE:    0 internal server task,1 remote task
        *   VALUE:    func name which be called
        *   TIME:    when to do : 0 once  , relay to the CYCLE
            CYCLE:  lifecycle of job   day,week,month
            TARGET:    unique identify for server or instance or database.  
                       unique command type when in the case used for remote command etc.
                           *cmd
                           *python
                           *bash
            ARGS:    args for the api func
            TOOL:    Internal func calls
        '''
        _d=None
        if type(data) == types.DictionaryType:
            _d=dict(TCP_HEADER,**data)
        elif type(data) == types.StringType:
            _d=dict(TCP_HEADER,**eval(data))
        else:
            _d={}
        _item=['TYPE','TIME','VALUE','CYCLE','TARGET','ARGS']
        for _i in _item:
            if not _d.get(_i):
                _d[_i]=DEFAULT_NONE            
        return _d
    
    def _data_unpack(self,data):
        if not data:
            return ''
        return data.replace(END_SIGN,'')
    
    def close(self):
        self.s.close()   


class MegaTool():

    def __init__(self):
        pass

    def get_all_funcs(self):
        cmd='get_all_funcs'
        self.c=MegaClient(cmd=cmd)
        func_list=self.c.run(TOOL=True)
        if func_list:
            i=1
            for f in eval(func_list):
                print i,f['name'],f['args']
                i+=1
        self.close()
    
    def close(self):
        self.c.close

def get_help():
    print 'usage:'
    print 'python sender.py [help] -get this doc'
    print 'python sender.py list -get all the supported fucntion and description'
    print  MegaClient().__doc__
    

if __name__=="__main__":
    import sys
    cmd=''
    if len(sys.argv)>1:
        cmd=sys.argv[1]
        if cmd.upper()=='LIST':
            t=MegaTool()
            t.get_all_funcs()
#for test
        elif cmd.upper() == 'HELP' or '-H':
            get_help()
        else:
            cmd='get_all_instance'
            c=MegaClient(cmd=cmd)
            if c:
                print c.run(func_args="model='backup',stat=1,role=1",CYCLE=1)
                c.close()
    else:
        get_help()
