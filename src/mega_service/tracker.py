import time
import multiprocessing
from lib.logs import Logger
from lib.PyMysql import PyMySQL
from mega_service.task import Task
from conf.settings import TRACKER_LIFCYCLE

MODEL='Tracker'
log=Logger(MODEL).log()

class Tracker():
    def __init__(self,queue):
        '''
            Two type tasks would be tracked :
            1.cycle task on the specified time
            2.realtime task need to be retry
        '''
        self.queue=queue  
        self.q=PyMySQL()
  
    def tracker(self):
        self._name=multiprocessing.current_process().name
        log.info("%s is Starting..." % self._name)           
        data=None
        while 1:
            try:
                data=self.routine_task()
                for d in data:
                    self.queue.put(d)
                time.sleep(TRACKER_LIFCYCLE)
            except Exception as ex:
                log.error(ex)
    
    def routine_task(self):
        _task=[]
        _t={}
        now=time.strftime('%H:%M',time.localtime(time.time()))
        sql="select * from task where timestampdiff(second,last_time,now())>=cycle;"
        for t in self.q.fetchAll(sql):
            _t["ARGS"]="'"+str(now)+"'" # use to update the config table in api.mange
            _t["NAME"]=t[1]
            _t["TYPE"]=t[2]
            _t["VALUE"]=t[3]
            _t["LAST_TIME"]=t[4]
            _t["CYCLE"]=t[5]
            _t["TIME"]=0   #realtime jobs
            _task.append(_t)
            #update the last_time of task up to now
            Task().stat_task_by_id(t[0])
        if _task:
            log.debug(_task)
        return _task
    
    def retry_task(self):
        return 
        