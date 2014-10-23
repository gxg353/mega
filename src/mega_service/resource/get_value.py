# -*- coding:utf-8 -*-
'''
Created on Oct 20, 2014

@author: xchliu

@module:mega_service.resource.test
'''
from lib.PyMysql import PyMySQL

def get_instance_newest_stat(instance_id,stat): 
    q=PyMySQL()       
    sql="select b.value from status a,status_his b where a.id=b.status_id and b.instance_id=%s and \
        a.name='%s' order by b.id desc limit 1;" % (instance_id,stat)
    result=q.fetchRow(sql)
    if result:
        result=result[0]
    else:
        result=0
    return result

def get_instance_newest_variable(instance_id,var): 
    q=PyMySQL()       
    sql="select b.value from variables a,variables_his b where a.id=b.variable_id and b.instance_id=%s and \
        a.name='%s' order by b.id desc limit 1;" % (instance_id,var)
    result=q.fetchRow(sql)
    if result:
        result=result[0]
    else:
        result=0
    return result


def main():
    return
if __name__ == "__main__":
    main()