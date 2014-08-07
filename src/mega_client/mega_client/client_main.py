# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_service.mega_client.client_main
'''
import datetime
import multiprocessing

from listener import tcp_server
from logs import Logger
from worker import Monitor

MODEL='ClientMain'
log = Logger(MODEL).log()




def main(): 
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
        t.start()
        child_pids.append(t.pid)
    log.debug("Sub processes: %s" %child_pids)
    return child_pids
    
if __name__=='__main__':
    main()