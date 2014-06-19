# -*- coding: UTF-8 -*-
#Change LOG

import sys
sys.path.append('..')
import socket
import types

TCP_HEADER={'HEAD':'MEGA'}
END_SIGN='EOF'
BUFFER_SIZE=10
DEFAULT_NONE=0
HEADER_LENGTH=10


class MegaClient():
    def __init__(self,host='localhost',port=1104,cmd=''):
        self._cmd={}
        self.host=host
        self.port=port
        if cmd:
            self._cmd['VALUE']=str(cmd)
    def run(self,func_args=None,**args):
        if not self._cmd:
            return False
        if self.conn():
            if func_args:
                self._cmd['ARGS']=str(func_args)
            if len(args)>0:
                self._cmd=dict(self._cmd,**args)
            
            _d=self.cmd_run(self._cmd)
        else:
            _d=None
        return _d
    def conn(self):
        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      
            self.s.connect((self.host,self.port))
            return self.s
        except Exception as ex:
            print ex
#           log.error('Connect to server failed as : %s' % ex)
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
            else:
                data=False
            return self._data_unpack(data)
        except Exception as ex:
            print ex
#            log.error("Interactive failed as : %s" % ex)
    def _cmd_pack(self,data):
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
            return False
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
    def close(self):
        c.close

if __name__=="__main__":
    cmd=''
    if len(sys.argv)>1:
        cmd=sys.argv[1]
    if cmd.upper()=='HELP':
        t=MegaTool()
        t.get_all_funcs()
#for test
    else:
        cmd='get_all_instance'
        c=MegaClient(cmd=cmd)
        if c:
            print c.run(func_args="model='backup',stat=1,role=1",CYCLE=1)
            c.close()
    