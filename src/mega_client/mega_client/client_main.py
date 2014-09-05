# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_service.mega_client.client_main
'''
import os
import sys
import time
import datetime
import multiprocessing

app_path=os.path.dirname(sys.path[0])
sys.path.append(app_path)

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

    #restart the subprocess if error occur
    for pid in child_pids:
        file(pidfile,'a+').write("%s\n" % pid)
             
    while 1:
        time.sleep(10)
        try:
            for t in thread:
                if t.is_alive() == False:
                    if t.pid in child_pids:
                        child_pids.remove(t.pid)
                    t.start()
                    child_pids.append(t.pid)
                    if pidfile:
                        for pid in child_pids:
                            file(pidfile,'w+').write("%s\n" % t.pid)
                    
        except Exception as ex:
            log.error(ex)
            break
    return child_pids
    
if __name__=='__main__':
    main()