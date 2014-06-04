import time
import types
import multiprocessing
from lib.logs import Logger
from apis.resource import * 

MODEL='Worker'
log = Logger(MODEL).log()

class Worker():
    def __init__(self,queue):
        self.queue=queue    
    def worker(self):
        self._name=multiprocessing.current_process().name
        log.info("%s is Working..." % self._name)           
        data=None
        while 1:
            try:
                if not self.queue.empty():
                    data=self.queue.get()
                    if data:
                        self.work_deliver(data)
                time.sleep(1)
            except KeyboardInterrupt:
                log.error("%s is Quitting..." % self._name)
                break
    def work_resolve(self,data):
        """        work instance:{'HEAD':'MEGA','TYPE':'CMD','VALUE':'ls'}
        keys:
        *    HEAD:    for safe interactive,should be MEGA
        *   TYPE:    0 internal server task,1 remote task
        *   VALUE:   what to do : ls
        *   TIME:    when to do : 0 once  ,
            CYCLE:  lifecycle of job   day,week,month
            TARGET:    unique identify for server or instance or database.
        """
        if len(data)==0:
            return False
        d=None
        try :
#            print data
#            d=simplejson.loads(data)
            d=eval(data)
            if type(d)== types.DictionaryType:
                if not (d.has_key('TYPE') or d.has_key('VALUE')):
                    return False
            else:
                return False
        except Exception as ex:
            log.error("Resolve the data failed as : %s" % ex)
        self.task=d
        return True
        
    def work_deliver(self,work):
    #1.run the command
    #2.save task into db
        if not self.work_resolve(work):
            print 1
            return False
        #real time job
        #print self.task.get('TIME')
        if self.task.get('TIME') == 0:
        #subthread
            result=Executor_Local(self.task.get('VALUE')).do_cmd(self.task.get('ARGS'))
        else:
        #save into db
            pass
        return result
    def close(self):
        self.close()

class Executor_remote():
    '''
     Run the task on the remote server in subprocess
    '''
    def __init__(self):
        pass
    def run(self):
        pass
    def salt_loader(self):
        pass
class Executor_Local():
    def __init__(self,cmd):
        self.cmd=cmd
    def do_cmd(self,func_args=None):
#        func=getattr(resource,self.cmd,None)
        print func_args
        return eval("%s(%s)" % (self.cmd,func_args))
        #return func(func_args.split(','))
#mark  do the command
#return all the funcs


class Saver():
    '''
    save task into database if it need to be rerun  
    '''
    def __init__(self):
        pass
    def run(self):
        pass