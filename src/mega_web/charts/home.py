# -*- coding:utf-8 -*-
'''
Created on Aug 18, 2014

@author: xchliu

@module:mega_web.charts.home
'''
from lib.PyMysql import PyMySQL
from lib.utils import today
from chart import Chart


def get_slowlog_report(request):
    sql="select day(stattime) as day,sum(counts) as counts from report_slowlog  where date(stattime) between '%s' and '%s' group by date(stattime);" % (today(7),today())
    cursor=PyMySQL().query(sql)
    data=cursor.fetchall()
    c=Chart()
    c.yaxis_name='counts'
    c.data_list=["counts",]
    return c.generate(data, 'slow log')
    
def main():
    return
if __name__ == "__main__":
    main()