# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
import socket
import multiprocessing   
import SocketServer
from SocketServer import StreamRequestHandler as SRH
from conf.GlobalConf import DEFAULT_TCP_PORT,DEFAULT_TCP_HOST,DEBUG
from lib.logs import Logger
from worker import Worker

END_SIGN='EOF'
ERROR='-1'
SUCCESS='0'
TCP_HEADER=['HEAD','MEGA']
BUFFER_SIZE=10
HEADER_LENGTH=10

MODEL='Listener'
log = Logger(MODEL).log()


def tcp_listen(queue,host='',port=555):
    _name=multiprocessing.current_process().name    
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host,port))   
    s.listen(10)
#    print "%s Listen on %s:%s" %(_name,host,port)
    while 1:
        try:
            conn,addr=s.accept()            
            print _name,'Connected by' ,addr    
            while True:    
                data=conn.recv(1024)    
                print data
                if not queue.full():
                    queue.put(data)
                conn.sendall('END')   
            conn.close()
        except Exception as ex:
            print(ex)
            conn.close()
    s.close()


 
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
        data=data.replace('EOF', '')
        if DEBUG:
            log.debug(data)
            q.put(data)
        if self.data_check(data):
            _w=Worker(None).work_deliver(data)
            result=str(_w)

            q.put(data)
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
            
    def data_check(self,data):
        if len(data) == 0:
            return False
        try:
            if eval(data).get(TCP_HEADER[0]).upper() != TCP_HEADER[1]:
                return False
        except:
            return False
        return True
        
def tcp_server(queue,host=DEFAULT_TCP_HOST,port=DEFAULT_TCP_PORT):
    global q
    q=queue
    addr = (host,port)
    log.info('TCP Server listen on %s ...' % str(addr))
    try:  
        server = SocketServer.ThreadingTCPServer(addr,Servers)
        server.serve_forever()
    except Exception as ex:
        log.error('TCP server start failed as: %s',ex)
        sys.exit(1)


if __name__=="__main__":
    tcp_server()