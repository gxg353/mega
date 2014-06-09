import datetime
import multiprocessing
from listener import tcp_server
from worker import Worker 
from lib.logs import Logger
from backup.Backuper import backuper

MODEL='MAIN'
log=Logger(MODEL).log()

def sub_process():
    global queue
    queue = multiprocessing.Queue()
    worker=Worker(queue).worker
    threads=[]
    try:
        log.debug('Start Subprocess: ')
        workers=multiprocessing.Process(target=worker,args=(),name="Main Worker")
        threads.append(workers)
        listens=multiprocessing.Process(target=tcp_server,args=(queue,),name="TCP Listener")
        threads.append(listens)
        backuper=multiprocessing.Process(target=backuper,args=(),name="Backup worker")
        threads.append(backuper)

        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        log.debug('Get interrupt from keyboard,quit now')
        return
 
def main():
    log.info('Mega server start at %s ' % datetime.datetime.now())
    sub_process()
if __name__ == "__main__":
    main()

