# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
import socket
import types

TCP_HEADER={'HEAD':'MEGA'}
END_SIGN='EOF'
BUFFER_SIZE=10
DEFAULT_NONE=0


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
        try:
            cmd_with_pack=self._cmd_pack(cmd)
            if cmd_with_pack:
                self.s.sendall(str(cmd_with_pack))
                while 1:
                    _d=self.s.recv(BUFFER_SIZE)
                    data+=_d
                    if _d.find(END_SIGN) > 0:
                        break
            else:
                data='-1'
            return data
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
    def close(self):
        self.s.close()   

if __name__=="__main__":
#    cmd=sys.argv[1]
    cmd='get_all_instance'
    c=MegaClient(cmd=cmd)
    if c:
        print c.run(func_args='stat=1,role=1',CYCLE=1)
        c.close()