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
        