# -*- coding:utf-8 -*-
'''
Created on Aug 19, 2014

@author: xchliu

@module:mega_web.tunning.slowlog
'''
from lib.PyMysql import PyMySQL
from mega_web.charts.chart import Chart
from lib.utils import today

cursor=PyMySQL()
    

def get_chart_groupbyinstance():
    sql=''' select concat(ip,':',port),sum(counts) as counts from slowlog_day a,instance b where a.instance_id=b.id and   
        date(stattime) between '%s' and '%s' group by instance_id order by counts desc limit 10;''' % (today(7),today())
    data=cursor.query(sql).fetchall()
    c=Chart()
    c.type='column'
    c.yaxis_name='counts'
    c.data_list=["counts",]
    return c.generate(data, 'slow log by instance') 

def get_chart_total():
    sql="select day(stattime) as day,sum(counts) as counts from slowlog_day  where date(stattime) between '%s' and '%s' group by date(stattime);" % (today(7),today())
    cursor=PyMySQL().query(sql)
    data=cursor.fetchall()
    c=Chart()
    c.yaxis_name='counts'
    c.data_list=["counts",]
    return c.generate(data, '')

def get_chart_groupbytime():
    sql='''select date(stattime) as day,sum(lt_one) as lt_one,sum(lt_five) as lt_five,sum(lt_ten) as lt_ten,sum(lt_hundred) as lt_hundred,sum(gt_hundred) as gt_hundred  from slowlog_time_hour
         where date(stattime) between '%s' and '%s' group by hour(stattime);''' % (today(7),today())
    data=cursor.query(sql).fetchall()
    c=Chart()
    c.type='pie'
    c.yaxis_name='counts'
    c.data_list=["<1s","<5s","<10s","<100s",">100s"]
    return c.generate(data, 'slow log by time') 

def get_chart_topsql():
    sql="select hash_code,sql_parse,counts,max_time,min_time,avg_time,max_row,min_row,avg_row from slowlog_archive_hour where date(log_time) between '%s' and '%s' order by counts desc limit 100 ;" % (today(7),today())
    data=cursor.query(sql,type='dict').fetchall()
    return data

def main():
    return
if __name__ == "__main__":
    main()