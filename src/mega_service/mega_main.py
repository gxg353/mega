import datetime
import multiprocessing
from listener import tcp_server
from worker import Worker
from tracker import  Tracker
from lib.logs import Logger

MODEL='MAIN'
log=Logger(MODEL).log()



class SubProcess:
    def __init__(self):
        self.threads=[]
        self.child_pids=[]

    #===========================================================================
    # sub_process
    # Start the child processes:
    #    1.worker         Resolve and do the jobs 
    #    2.listens        Accept task from mega sender 
    #    3.trackers       Track task from database
    #    4.monitor        Internal monitor 
    #===========================================================================
    def sub_process(self,pidfile):
        global queue
        queue = multiprocessing.Queue()
        worker=Worker(queue,).worker
        tracker=Tracker(queue).tracker
        try:
            log.info('Start Subprocess: ')
            
            workers=multiprocessing.Process(target=worker,args=(),name="Main Worker")
            self.threads.append(workers)
            
            listeners=multiprocessing.Process(target=tcp_server,args=(queue,),name="TCP Listener")        
            self.threads.append(listeners)
            
            trackers=multiprocessing.Process(target=tracker,args=(),name="Tracker")
            self.threads.append(trackers)                      
            
            monitor=multiprocessing.Process(target=self.monitor,args=(),name="Monitor")
            self.threads.append(monitor)
            #backuper=multiprocessing.Process(target=backuper,args=(),name="Backup worker")
            #threads.append(backuper)        
            for t in self.threads:
               # t.daemon=True
                t.start()
                self.child_pids.append(t.pid)
                log.info([t.name,t.pid])
                if pidfile:
                    file(pidfile,'a+').write("%s\n" % t.pid)
            for t in self.threads:
                t.join()
        except Exception as ex:
            log.warning('Get interrupt signal,quit now!')
            log.error(ex)
        self.pool_close()
        return self.child_pids
    
    #===========================================================================
    # monitor
    #===========================================================================
    def monitor(self):
        log.debug(self.child_pids)
    

    
def main(pidfile):
    log.info("=============BEGIN===========")
    log.info('Mega server start at %s ' % datetime.datetime.now())
    SubProcess().sub_process(pidfile)

if __name__ == "__main__":
        main()

