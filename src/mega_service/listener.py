# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
import socket
import multiprocessing   
import SocketServer
from SocketServer import StreamRequestHandler as SRH
from conf.GlobalConf import DEFAULT_TCP_PORT,DEFAULT_TCP_HOST,DEBUG
from lib.logs import Logger

ERROR='-1'
SUCCESS='0'
TCP_HEADER=['HEAD','MEGA']
MODEL='Listener'
log = Logger(MODEL).log()

def tcp_listen(queue,host='',port=555):
    _name=multiprocessing.current_process().name    
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host,port))   
    s.listen(10)
    print "%s Listen on %s:%s" %(_name,host,port)
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
        while True:
            data = self.request.recv(1024)
            if not data: 
                break
            if DEBUG:
                log.debug(data)
                q.put(data)
            if self.data_check(data):
                result=SUCCESS
                q.put(data)
            else:
                result=ERROR 
            self.request.send(result)
            
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
    log.info('TCP server listen on %s ...' % str(addr))
    try:  
        server = SocketServer.ThreadingTCPServer(addr,Servers)
        server.serve_forever()
    except Exception as ex:
        log.error('TCP server start failed as: %s',ex)
        sys.exit(1)


if __name__=="__main__":
    tcp_server()