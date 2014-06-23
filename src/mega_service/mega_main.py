import sys
sys.path.append("..")
import datetime
import multiprocessing
from listener import tcp_server
from worker import Worker
from tracker import  Tracker
from lib.logs import Logger
#from backup.Backuper import backuper

MODEL='MAIN'
log=Logger(MODEL).log()
class SubProcess:
    def __init__(self):
        self.threads=[]
        self.child_pids=[]
    def sub_process(self):
        global queue
        queue = multiprocessing.Queue()
        worker=Worker(queue).worker
        tracker=Tracker(queue).tracker
        try:
            log.info('Start Subprocess: ')
            workers=multiprocessing.Process(target=worker,args=(),name="Main Worker")
            self.threads.append(workers)
            self.listens=multiprocessing.Process(target=tcp_server,args=(queue,),name="TCP Listener")        
            self.threads.append(self.listens)
            self.trackers=multiprocessing.Process(target=tracker,args=(),name="Tracker")
            self.threads.append(self.trackers)
           
            #backuper=multiprocessing.Process(target=backuper,args=(),name="Backup worker")
            #threads.append(backuper)        
            for t in self.threads:
                t.start()
                self.child_pids.append(t.pid)
            log.debug(self.child_pids)
            #for t in self.threads:
            #    t.join()
        except Exception as ex:
            log.debug('Get interrupt from keyboard,quit now')
            log.error(ex)
        return self.child_pids
def main():
    log.info("=============BEGIN===========")
    log.info('Mega server start at %s ' % datetime.datetime.now())
    child_pid_list=SubProcess().sub_process()
    return child_pid_list
if __name__ == "__main__":
    if len(sys.argv) >1: 
        pid_file=sys.argv[1]
    main(pid_file)

