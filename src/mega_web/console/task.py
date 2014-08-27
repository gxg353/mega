# -*- coding:utf-8 -*-
'''
Created on Aug 4, 2014

@author: xchliu

@module:mega_web.console.task
'''

import datetime
from mega_web.entity.models import Task
from mega_web.entity.models import User

DEFAULT_TASK_CYCLE=120


class TaskManage():
    def __init__(self,task):
        self.task=task
        self.t=Task()
        self.task_id=self.task.get('id')
        self.task_name=self.task.get('task_name')
        self.task_type=self.task.get('task_type')
        self.task_value=self.task.get('task_value')
        self.task_script=self.task.get('task_script')
        self.task_cycle=self.task.get('task_cycle')
        self.task_target=self.task.get('task_target')
        self.task_owner=self.task.get('task_owner')
        self.task_stat=self.task.get('task_stat')
    
    def task_add(self):
        if not self.task_value and not self.task_script:
            return -1,'Value or script should be provided'
        if self.task_name:
            self.t.name=self.task_name
        else:
            self.t.name=self.task_value
        self.t.type=self.task_type
        self.t.value=self.task_value
        self.t.script=self.task_script
        if self.task_cycle:
            self.t.cycle=self.task_cycle
        else:
            self.t.cycle=DEFAULT_TASK_CYCLE
        
        self.t.target=self.task_target
        self.t.owner=self.task_owner
        self.t.stat=self.task_stat
        _now=datetime.datetime.now()
        self.t.last_time=_now
        self.t.create_time=_now
        self.t.save()
        
        return 1,'Success'
    
    def task_mod(self):
        if not self.task_id:
            return False
        _task=Task.objects.get(id=self.task_id)
        if not self.task_value and not self.task_script:
            return -1,'Value or script should be provided'
        if self.task_name:
            _task.name=self.task_name
        else:
            _task.name=self.task_value
        _task.type=self.task_type
        _task.value=self.task_value
        _task.script=self.task_script
        if self.task_cycle:
            _task.cycle=self.task_cycle
        else:
            _task.cycle=DEFAULT_TASK_CYCLE
        
        _task.target=self.task_target
        _task.owner=self.task_owner
        _task.stat=self.task_stat
        _task.save()
        return 1,'success'

    
    def get_task_by_id(self):
        task=Task.objects.filter(id=self.task_id).values()
        if task:
            task=task[0]
        owner=User.objects.filter(id=task['owner']).values('name')[0]
        task['owner_name']=owner['name']
        return task
        
        
def main():
    return
if __name__ == "__main__":
    main()