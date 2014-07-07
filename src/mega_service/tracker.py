import multiprocessing
import time
from lib.logs import Logger
from lib.PyMysql import PyMySQL
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
        try:
            while 1:
                data=self.routine_task()
                for d in data:
                    self.queue.put(d)
                time.sleep(TRACKER_LIFCYCLE)
        except KeyboardInterrupt:
            log.error("%s is Quitting..." % self._name)
    
    def routine_task(self):
        _task=[]
        _t={}
        now=time.strftime('%H:%M',time.localtime(time.time()))
        sql="select * from task where timestampdiff(second,last_time,now())>=cycle;"
        for t in self.q.fetchAll(sql):
            _t["ARGS"]=str(t[0])+",'"+str(now)+"'" #id  use to update the config table in api.mange
            _t["NAME"]=t[1]
            _t["TYPE"]=t[2]
            _t["VALUE"]=t[3]
            _t["LAST_TIME"]=t[4]
            _t["CYCLE"]=t[5]
            _t["TIME"]=0
            _task.append(_t)
        if _task:
            log.debug(_task)
        return _task
    
    def retry_task(self):
        return 
        