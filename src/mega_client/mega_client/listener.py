# -*- coding: UTF-8 -*-
import time,sys
import SocketServer
import signal
from SocketServer import StreamRequestHandler as SRH
from setting import TCP_HOST,TCP_PORT
from logs import Logger
from worker import Worker

END_SIGN='eof'.upper()
ERROR='-1'
SUCCESS='0'
TCP_HEADER=['HEAD','MEGA']
BUFFER_SIZE=10
HEADER_LENGTH=10

MODEL='Listener'
log = Logger(MODEL).log()
 
SocketServer.ThreadingTCPServer.allow_reuse_address = True

class Servers(SRH):
    
    def handle(self):
        log.debug('Get connection from %s' % str(self.client_address))
        global q
        result=''
        data=''
        header=''
        header=int(self.request.recv(HEADER_LENGTH))
        while header>0:
            _d= self.request.recv(BUFFER_SIZE)
            data+=_d
            if _d.find(END_SIGN) > 0:
                break
            header=header-BUFFER_SIZE
#            print header,_d
        data=data.replace(END_SIGN, '')
        log.debug(data)
        if self.data_check(data):
            _w=Worker(data).run()
            result=str(_w)
        else:
            result=ERROR
#todo : 
#    get the len(result),add the length to the head of packget, 
#    chancel the end sign
        _len=len(result)+HEADER_LENGTH
        _header=str(_len)
        for i in range(HEADER_LENGTH - len(str(_len))):
            _header='0'+_header
        self.request.sendall(_header+result+END_SIGN)
        self.request.close()
            
    def data_check(self,data):
        if len(data) == 0:
            return False
        try:
            if eval(data).get(TCP_HEADER[0]).upper() != TCP_HEADER[1]:
                return False
        except:
            return False
        
        return True
        
def tcp_server(host=TCP_HOST,port=TCP_PORT):
    
    def sign_killed(signum,frame):
        server.server_close()
        log.info("TCP server quiting...")
        sys.exit(0)

    addr = (host,port)
    log.info('TCP Server listen on %s ...' % str(addr))
    server=None
    signal.signal(signal.SIGINT, sign_killed)
    signal.signal(signal.SIGTERM, sign_killed)

    try:
        server = SocketServer.ThreadingTCPServer(addr,Servers)
        server.daemon_threads=True
        server.serve_forever()
        
    except Exception as ex:
        log.error('TCP server start failed as: %s',ex)
        sys.exit(1)
    finally:
        if server:
            server.shutdown()
            server.server_close()
    
        
        
if __name__=="__main__":
    tcp_server()