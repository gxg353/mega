# -*- coding:utf-8 -*-
'''
Created on Jul 16, 2014

@author: xchliu

@module:mega_service.slow_log
'''
from apis.api import get_all_instance

class SlowLog():

    def __init__(self):
        pass
    
    def get_instance_list(self):
        instance_list,error_code=get_all_instance(model='slowlog',stat=1)
        if error_code == 0:
            return instance_list
        else:
            return []