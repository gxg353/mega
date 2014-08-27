# -*- coding:utf-8 -*-
'''
Created on Jul 16, 2014

@author: xchliu

@module:mega_service.slow_log
'''
from lib.PyMysql import PyMySQL

class SlowLog():

    def __init__(self):
        pass
    
    def get_slowlog_instance_list(self):
        sql="select * from instance where stat=1 and slowlog=1"
        instance_list=PyMySQL().query(sql, type='dict').fetchall()
        if instance_list:
            return instance_list
        else:
            return []