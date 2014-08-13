# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_service.mega_client.client_main
'''
import time
import datetime
import multiprocessing

from listener import tcp_server
from logs import Logger
from worker import Monitor

MODEL='ClientMain'
log = Logger(MODEL).log()




def main(pidfile=None): 
    log.info("=============BEGIN===========")
    log.info('Mega Client server start at %s ' % datetime.datetime.now())
    thread=[]
    child_pids=[]
    try:
        monitor=multiprocessing.Process(target=Monitor().monitor,args=(),name="Client Monitor")
        thread.append(monitor)
        listener=multiprocessing.Process(target=tcp_server,args=(),name='Client Listener')
        thread.append(listener)
    except Exception as ex:
        log.error(ex)
    for t in thread:
        t.daemon=True
        t.start()
        child_pids.append(t.pid)
        log.info((t.pid,t.name))
        if pidfile:
            file(pidfile,'a+').write("%s\n" % t.pid)
    time.sleep(10)
    #restart the tcp server if error return  
    if listener.is_alive() == False and listener.exitcode==1:
        _listener=multiprocessing.Process(target=tcp_server,args=(),name='Client Listener')
        _listener.start()
        thread.append(_listener)
    for t in thread:
        t.join()
    return child_pids
    
if __name__=='__main__':
    main()