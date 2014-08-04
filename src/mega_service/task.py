from lib.PyMysql import PyMySQL


class Task():
    def __init__(self):
        self.q=PyMySQL()
    def stat_task_by_id(self,id,stat_time=0):
        if stat_time == 0:
            sql="update task set last_time=now() where id=%s" % id
            if self.q.execute(sql):
                return True
        return False
    
    def get_task_by_name(self,name):
        if name:
            sql="select script from task where name='%s'" % name
            return self.q.fetchOne(sql)
        else:
            return False
        
    def get_task_list(self,stat=1):
        if stat == -1 :
            sql="select * from task"
        else:
            sql="select * from task where stat=%s" % stat
        return self.q.fetchAll(sql)