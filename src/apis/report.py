# -*- coding:utf-8 -*-
'''
Created on Sep 24, 2014

@author: xchliu

@module:apis.report
'''

import datetime
from mega_service.report import daily 

def report_routine(time=None):
    #daily
    if not time:
        time=datetime.datetime.now().strftime('%H:%M')
    if int(time.split(':')[0]) == 10 :
        daily.backup_report_daily()

def main():
    return
if __name__ == "__main__":
    main()