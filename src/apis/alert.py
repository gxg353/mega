# -*- coding:utf-8 -*-
'''
Created on Sep 24, 2014

@author: xchliu

@module:apis.alert
'''
import sys
sys.path.append('/Users/xchliu/Documents/workspace/mega/src')


import datetime
from lib.logs import Logger
from lib.utils import today
from mega_web.console.backup import Backup 
from mega_web.entity.models import Alert

MODEL='API-Alert'
log = Logger(MODEL).log()

def alert_routine_hour(time=None):
    '''
        must be called only once in an hour 
    '''
    if not time:
        time=datetime.datetime.now().strftime('%H:%M')
    hour,minite=time.split(':')    
    #backup
    backup=Backup()
    failed_backup=backup.get_failed_backup(time)
    #only check once per day for daily task 
    if int(hour)==9:
        uninvoked_backup=backup.get_uninvoked_backup(today(1))
        unaviable_backup=backup.get_unavailable_backup()
    pack_alert('backup',uninvoked_backup,level=1,stat=0,head='uninvoked backup:')
    pack_alert('backup',unaviable_backup,level=1,stat=0,head='unaviable backup:')
    pack_alert('backup',failed_backup,level=1,stat=0,head='failed backup:')

def pack_alert(model,data,level=1,stat=0,head=''):
    if not data or not model:
        return
    result={
            'target':None,
            'model':model,
            'level':level,
            'stat':stat,
            'msg':None
            }
    for d in data:
        result['target']=':'.join([str(x) for x in d[1:3]])
        result['msg']=head+'-'.join([str(x) for x in d[3:-1]])
        res,ex=Alert(result).add_alert()
        if not res:
            log.warn(ex)

def main():
    alert_routine_hour()
if __name__ == "__main__":
    main()