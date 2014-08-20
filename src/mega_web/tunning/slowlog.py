# -*- coding:utf-8 -*-
'''
Created on Aug 19, 2014

@author: xchliu

@module:mega_web.tunning.slowlog
'''
from lib.PyMysql import PyMySQL
from mega_web.charts.chart import Chart
from lib.utils import today


def get_chart_groupbyinstance():
    sql=''' select ip,port,sum(counts) as counts from report_slowlog a,instance b where a.instance_id=b.id and   
        date(stattime) between '%s' and '%s' group by instance_id order by counts desc;''' % (today(7),today())
    cursor=PyMySQL().query(sql)
    data=cursor.fetchall()
    c=Chart()
    c.type='column'
    c.yaxis_name='counts'
    c.data_list=["counts",]
    return c.generate(data, 'slow log by instance') 


def main():
    return
if __name__ == "__main__":
    main()