import time
import types
import inspect
import multiprocessing
from lib.logs import Logger
from apis import api as apis

MODEL='Worker'
log = Logger(MODEL).log()


#===============================================================================
# _get_func_list
#===============================================================================
def _get_func_list(object):
        _funcs=[]
        if not object:
            return _funcs   
        for o in dir(object):
            obj_func=getattr(object,o,None)
            if inspect.isfunction(obj_func):
                _funcs.append({"name":"%s" % obj_func.__name__,"args":"%s" % str(inspect.getargspec(obj_func))})                 
        return _funcs    

class Worker():
    def __init__(self,queue):
        self.queue=queue    
    def worker(self):
        self._name=multiprocessing.current_process().name
        log.info("%s is Starting..." % self._name)           
        data=None
        while 1:
            try:
                if not self.queue.empty():
                    data=self.queue.get()
                    if data:
                        log.debug(data)
#                        log.info('got task from the queue')
                        self.work_deliver(data)
                time.sleep(1)
            except Exception as ex:
                log.error(ex)
                break
    def work_resolve(self,data):
        '''
        work instance:{'HEAD':'MEGA','TYPE':'CMD','VALUE':'ls'}
        keys:
        *   HEAD:    for safe interactive,should be MEGA
        *   TYPE:    0 internal server task,1 remote task
        *   VALUE:   what to do : ls
        *   TIME:    when to do : 0 once  , relay to the CYCLE
            CYCLE:  lifecycle of job   day,week,month
            TARGET:    unique identify for server or instance or database.
            TOOL:    Internal func calls
            _item=['TYPE','TIME','VALUE','CYCLE','TARGET','ARGS']
        
        '''
        if len(data)==0:
            return False
        d=None
        try :
            if type(data) == types.DictionaryType:
                d=data
            else:
                d=eval(data)                
            if type(d)== types.DictionaryType:
                if not (d.has_key('TYPE') or d.has_key('VALUE')):
                    return False
                else:
                    for _d in d:
                        if type(d[_d]) == types.StringType:
                            d[_d].replace('\n','')
                            ' '.join(d[_d].split())
            else:
                return False
        except Exception as ex:
            log.error("Resolve the data failed as : %s" % ex)
            log.error(data)
            return False
        self.task=d
        return True
        
    def work_deliver(self,work):
    #1.run the command
    #2.save task into db
        if not self.work_resolve(work):
            log.error("Task resovle failed!")
            return False
        #internal funcs invoke,the task should include key : TOOL True
        if self.task.has_key('TOOL'):
            if self.task.get('VALUE')=='get_all_funcs':
                return _get_func_list(apis)

        #real time job    
        if self.task.get('TIME') == 0 :
        #subthread
            if self.task.get('TYPE')==0:
                result=Executor_Local(self.task.get('VALUE')).do_cmd(self.task.get('ARGS'))
            else:
                result=Executor_remote().run()
        else:
        #save into db
            self.queue.put(work)
            result=1
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
    '''
    request of mega server ,invoke func inside mega server
    '''
    def __init__(self,cmd):
        self.cmd=cmd
    def do_cmd(self,_args=None):
        func=getattr(apis,self.cmd,None)
        if func:
            log.debug("Call API: apis.%s(%s)" % (self.cmd,_args))
            return eval("apis.%s(%s)" % (self.cmd,_args))
        else:
            log.error("Function %s not found" % self.cmd)
            return False


class Saver():
    '''
    save task into database if it need to be rerun  
    '''
    def __init__(self):
        pass
    def run(self):
        pass