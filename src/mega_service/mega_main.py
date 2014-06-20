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

def sub_process():
    global queue
    queue = multiprocessing.Queue()
    worker=Worker(queue).worker
    tracker=Tracker(queue).tracker
    threads=[]
    try:
        log.debug('Start Subprocess: ')
        workers=multiprocessing.Process(target=worker,args=(),name="Main Worker")
        threads.append(workers)
        listens=multiprocessing.Process(target=tcp_server,args=(queue,),name="TCP Listener")
        
        threads.append(listens)
        trackers=multiprocessing.Process(target=tracker,args=(),name="Tracker")
        threads.append(trackers)
        #backuper=multiprocessing.Process(target=backuper,args=(),name="Backup worker")
        #threads.append(backuper)
        
        for t in threads:
            t.start()
    except Exception as ex:
        log.debug('Get interrupt from keyboard,quit now')
        log.error(ex)
        return
    

def main():
    log.info("=============BEGIN===========")
    log.info('Mega server start at %s ' % datetime.datetime.now())

    sub_process()
    
if __name__ == "__main__":
    if len(sys.argv) >1: 
        pid_file=sys.argv[1]
    main(pid_file)

