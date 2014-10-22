# -*- coding:utf-8 -*-
'''
Created on Sep 25, 2014

@author: xchliu

@module:monitor.alter_manage
'''

from lib.PyMysql import PyMySQL

cursor=PyMySQL()

def get_alert_list():
    sql="select * from alert where stat=0 order by model,target;"
    return cursor.query(sql,type='dict').fetchall()

def update_alert(id):
    if not id :
        return False
    sql="update alert set stat=1 where id=%s" % id
    return cursor.execute(sql)

def main():
    return
if __name__ == "__main__":
    main()