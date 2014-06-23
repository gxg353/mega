# -*- coding:utf-8 -*-
'''
Created on Jun 23, 2014

@author: xchliu

@module:apis.test
'''
#!/usr/bin/env python

import datetime
import mysql.connector

today = datetime.date.today()
four_year_ago = (today - datetime.timedelta(days=4)).strftime('%Y%m%d')
yesterday = (today - datetime.timedelta(days=1)).strftime('%Y%m%d')

tbl_org = 'jd_order_xml'
tbl_arc = tbl_org + '_' + yesterday + '_archive'
tbl_old = tbl_org + '_' + four_year_ago

def get_mysql_conn(host, user, passwd, database, port, charset="utf8"):
    ''''''
    conn = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database, port=port, charset=charset)
    return conn

def fetchall(sql):
    ''''''
    conn = get_mysql_conn('localhost', 'dbadmin', 'isqpswxx', 'mysql', 3306)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    conn.close_conn()
    
    return rows
    
    
def get_rows(tbl):
    ''''''
    sql = "select TABLE_NAME from information_schema.TABLES where TABLE_NAME='{0}'".format(tbl)
    rows = fetchall(sql)
    return rows

def set_rows(tbl, autocommit=False):
    ''''''
    tbl_new = get_rows(tbl)
    conn = get_mysql_conn('172.17.62.37', 'dbchecksum', '', 'dbchecksum', 3308)
    if tbl_new == tbl_arc:
        sql_ins = "insert into dbchecksum.dbcheck(report_type_id,instance_id,db_name,time,status,level) \
        values(4,'62523306','all',{0},'Archive table {1} add Succeed','ok');".format(today, tbl)
        
    else:
        sql_ins = "insert into dbchecksum.dbcheck(report_type_id,instance_id,db_name,time,status,level) \
        values(4,'62523306','all',{0},'Archive table {1} add Failed','ok');".format(today, tbl)
    cursor = conn.cursor()
    if autocommit:
        cursor.execute("set autocommit=1")
    cursor.execute(sql_ins)
    conn.close_conn()
        
def close_conn(conn):
    ''''''
    conn.close()
    
if '__name__' == "__main__":
    ''''''
    print tbl_arc
    set_rows(tbl_arc)
    