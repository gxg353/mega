import time
from lib.logs import Logger
from mega_web.entity.models import Backup_Policy
from lib.PyMysql import PyMySQL

MODEL='BACKUP'
log=Logger(MODEL).log()

class Backuper():
    def __init__(self):
        self.backup_policy=Backup_Policy
        self.q=PyMySQL()
    def backuper(self,now=None):
        '''
        retrun the server list which need to run backup right now
        '''
        if not now:
            now=time.strftime('%H:%M',time.localtime(time.time()))
        server_list = self.get_task(now)
        return server_list

    def get_task(self,now):
        #daily ,weekly,monthly
        _data=[]
        _now={}
        _now["day"]=time.strftime('%H:%M',time.localtime(time.time()))
        _now["week"]=time.strftime('%a',time.localtime(time.time()))
        _now["month"]=time.strftime('%d',time.localtime(time.time()))
        for _n in _now:
            if _n == 'day':            
                sql="select * from backup_policy where cycle='%s' and schedule_time='%s' and is_schedule=1" %(_n,now)
            else:
                sql="select * from backup_policy where cycle='%s' and find_in_set('%s',backup_time) and schedule_time='%s' and is_schedule=1" %(_n,_now[_n],now)
            #_d=self.backup_policy    .objects.raw(sql)
            _d=self.q.fetchAll(sql)
            for _ob in _d:
                _data.append(_ob)
        if len(_data)>0:
            log.debug('Get backup task:')
            log.debug(_data)
        return _data
    
    def push_task(self):
        pass
    def log_task(self):
        pass
