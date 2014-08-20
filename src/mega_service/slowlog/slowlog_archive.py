# -*- coding:utf-8 -*-
'''
Created on Aug 20, 2014

@author: xchliu

@module:mega_service.slowlog.slowlog_archive
'''
from lib.sql_parse import SQLParse
from mega_web.resource.instance_manage import InstanceGet

def slowlog_statics_per_log(data):
    '''
        data : a slow log instance
        
        1.parse sql
        2.get the sql hash
        3.statics
    '''
    if not data:
        return False
    sql=data.get('sql_text')
    sql_parsed=SQLParse(sql).var_replace()
    sql_hash=hash(sql_parsed)
    instance_id=InstanceGet().get_instance_by_ip_port(data.get('db_host'), data.get('port'))
    #todo
def main():
    return
if __name__ == "__main__":
    main()