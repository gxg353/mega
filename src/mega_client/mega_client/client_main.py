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
    childs={"Client Monitor":Monitor().monitor,
            "Client Listener":tcp_server
            }
    try:
        for child in childs.items():
            c=sub_process(child)
            if c:
                thread.append(c)
    except Exception as ex:
        log.error(ex)
    
    for t in thread:
        t.daemon=True
        t.start()
        child_pids.append(t.pid)
        file(pidfile,'a+').write("%s\n" % t.pid)
        log.info((t.pid,t.name))

    
    #restart the subprocess if error occur             
    while 1:
        time.sleep(30)
        try:
            for t in thread:
                if t.is_alive() == False:
                    if t.pid in child_pids:
                        child_pids.remove(t.pid)
                    if t in thread:
                        thread.remove(t)
                    #try to restart the dead sub process
                    _t=sub_process((t.name,childs.get(t.name)))                    
                    thread.append(_t)
                    _t.start()                    
                    child_pids.append(_t.pid)
                    log.info((_t.pid,_t.name))
                    
                    #flush the pids into pid file
                    if pidfile:
                        f=open(pidfile,'w')
                        #f.truncate()
                        for pid in child_pids:
                            f.write("%s\n" % pid)
                        f.flush()
                        f.close()                    
        except Exception as ex:
            log.error(ex)
            break
    return child_pids

def sub_process(func):
    if not func:
        return False
    return multiprocessing.Process(target=func[1],args=(),name=func[0])
   
    
if __name__=='__main__':
    main()