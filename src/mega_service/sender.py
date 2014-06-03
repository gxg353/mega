# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
import socket
import types
from lib.logs import Logger
from conf.GlobalConf import TCP_HEADER
MODEL='Client'
log=Logger(MODEL).log()

class MegaClient():
    def __init__(self,host='localhost',port=1104):
        self.host=host
        self.port=port
    def conn(self):
        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      
            self.s.connect((self.host,self.port))
            return self.s
        except Exception as ex:
            log.error('Connect to server failed as : %s' % ex)
    def cmd(self,cmd=None):
        if not cmd:
            return False
        try:
            cmd_with_pack=self._cmd_pack(cmd)
            if cmd_with_pack:
                self.s.sendall(str(cmd_with_pack))
                data=self.s.recv(1024)
            else:
                data='-2'
            return data
        except Exception as ex:
            log.error("Interactive failed as : %s" % ex)
    def _cmd_pack(self,data):
        _d=None
        if type(data) == types.DictionaryType:
            _d=dict(TCP_HEADER,**data)
        elif type(data) == types.StringType:
            _d=dict(TCP_HEADER,**eval(data))
        else:
            _d=None
        return _d
    def close(self):
        self.s.close()   

if __name__=="__main__":
#    cmd=sys.argv[1]
    cmd={'HEAD':'MEGA','TYPE':0,'VALUE':'get_all','TIME':0}
    c=MegaClient()
    c.conn()
    print c.cmd(cmd)
    c.close()