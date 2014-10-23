# -*- coding:utf-8 -*-
'''
Created on Sep 24, 2014

@author: xchliu

@module:mega_service.monitor
'''
from lib.logs import Logger

MODEL='Monitor'
log=Logger(MODEL).log()

class Monitor():
    def __init__(self,queue):
        self.q=queue
    def bussiness_monitor(self):
        '''
            1.backup
            2.slowlog
        '''
        
        pass
    def sys_monitor(self):
        pass

def main():
    return
if __name__ == "__main__":
    main()