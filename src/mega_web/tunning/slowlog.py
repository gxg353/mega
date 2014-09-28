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
    

def get_chart_groupbyinstance(begin=None,end=None):
    #default recent 7 days
    if not begin or not  end:
        begin=today(7)
        end=today()
    sql=''' select concat(ip,':',port),sum(counts) as counts from slowlog_time_day a,instance b where a.instance_id=b.id and   
            date(log_time) between '%s' and '%s' group by instance_id order by counts desc limit 10;''' % (begin,end)
    data=cursor.query(sql).fetchall()
    c=Chart()
    c.type='column'
    c.yaxis_name='counts'
    c.data_list=["counts",]
    return c.generate(data, 'slow log by instance') 

def get_chart_total(instance_id=None,begin=None,end=None):
    if not begin or not  end:
        begin=today(7)
        end=today()
    if instance_id:
        sql="select day(log_time) as day,sum(counts) as counts from slowlog_time_day  where instance_id=%s and date(log_time) between '%s' and '%s'  \
            group by date(log_time);" % (instance_id,begin,end)        
    else:
        sql="select day(log_time) as day,sum(counts) as counts from slowlog_time_day  where date(log_time) between '%s' and '%s'  \
            group by date(log_time);" % (begin,end)
    cursor=PyMySQL().query(sql)
    data=cursor.fetchall()
    c=Chart()
    c.yaxis_name='counts'
    c.data_list=["counts",]
    return c.generate(data, '')

def get_chart_groupbytime(begin=None,end=None):
    if not begin or not  end:
        begin=today(7)
        end=today()
    
    sql='''select date(log_time) as day,sum(lt_one) as lt_one,sum(lt_five) as lt_five,sum(lt_ten) as lt_ten,sum(lt_hundred) as \
         lt_hundred,sum(gt_hundred) as gt_hundred  from slowlog_time_day
         where date(log_time) between '%s' and '%s' group by hour(log_time);''' % (begin,end)
    data=cursor.query(sql).fetchall()
    c=Chart()
    c.type='pie'
    c.yaxis_name='counts'
    c.data_list=["<1s","<5s","<10s","<100s",">100s"]
    return c.generate(data, 'slow log by time') 

def get_chart_topsql(begin=None,end=None):
    if not begin or not  end:
        begin=today(7)
        end=today()    
    sql="select b.hash_code,b.sql_parsed,sum(counts) as counts,max_time,min_time,avg(avg_time) as avg_time,max_row,min_row,avg(avg_row) as avg_row from slowlog_sql_hour a ,sql_format b \
              where a.hash_code=b.hash_code and date(log_time) between '%s' and '%s' group by a.hash_code order by counts desc limit 100 ;" % (begin,end)
         
    data=cursor.query(sql,type='dict').fetchall()
    for d in data:
        d['sql_parsed']=d['sql_parsed'].decode('utf-8', 'ignore')
        opt_count=0
        sql="select count(*) from slowlog_opt where hash_code='%s'" % d.get('hash_code')
        opt_count=cursor.fetchOne(sql)
        if opt_count:
            d['opt_count']=opt_count
    return data

def get_instance_topsql(instance_id,begin=None,end=None):
    if not begin or not  end:
        begin=today(7)
        end=today()
    
    sql="select a.hash_code,b.sql_parsed,count(*) as counts,max(query_time) as max_time,min(query_time) as min_time,avg(query_time) as avg_time,\
        max(rows_examined) as max_row,min(rows_examined) as min_row,avg(rows_examined) as avg_row from slowlog_info a ,sql_format  b where instance_id=%s \
        and a.hash_code=b.hash_code and date(from_unixtime(a.start_time)) between '%s' and '%s' group by a.hash_code order by counts desc;" %(instance_id,begin,end)
    data=cursor.query(sql,type='dict').fetchall()
    for d in data:
        d['sql_parsed']=d['sql_parsed'].decode('utf-8', 'ignore')
    return data


def get_sql_hosts(hash_code):
    sql="select concat(user,'@',user_host) as users,count(*) as counts from slowlog_info where hash_code='%s' group by user,user_host order by counts desc;" % hash_code
    data=cursor.query(sql).fetchall()
    c=Chart()
    c.type='column'
    c.yaxis_name='counts'
    c.data_list=["counts",]
    return c.generate(data, ' by instance') 

def get_sql_time(hash_code):
    sql="select date(log_time) as log_time,count(*) as counts from slowlog_sql_hour where hash_code='%s' group by date(log_time) order by date(log_time);" % hash_code
    data=cursor.query(sql).fetchall()
    c=Chart()
    c.yaxis_name='counts'
    c.data_list=["counts",]
    return c.generate(data, '')

def get_sql_info(hash_code):
    sql="select hash_code,db_host,port,dbname,sql_text,sql_explained from slowlog_info where hash_code='%s' limit 1" %hash_code
    data=cursor.query(sql,type='dict').fetchone()
    return data

def add_opt_record(request):
    hash_code=request.get('hash_code')
    opt_method=request.get('opt_method')
    opt_explain=request.get('opt_explain')
    if not hash_code:
        return 'Get sql hash code failed!'  
    if not opt_method:
        return 'Invalid optimize method'
    sql="insert into slowlog_opt(hash_code,opt_method,opt_explain,opt_time) values('%s','%s','%s',now())" %(hash_code,opt_method,opt_explain)
    result,ex=cursor.execute(sql)
    if not result:
        result=ex
    else:
        result='Success    '
    return result

def get_opt_record(hash_code):
    if not hash_code:
        return 
    sql="select * from slowlog_opt where hash_code='%s'" % hash_code
    data=cursor.query(sql,type='dict').fetchall()
    return data

def get_chart_groupbydb(instance_id=None,begin=None,end=None):
    if not begin or not  end:
        begin=today(7)
        end=today()
    if instance_id:
        sql='''select db,sum(counts) as counts from slowlog_time_day where instance_id=%s and date(log_time) between '%s'  and '%s' group by db ;
            ''' % (instance_id,begin,end)
    else:
        sql='''select db,sum(counts) as counts from slowlog_time_day where date(log_time) between '%s'  and '%s' group by db ;
            ''' % (begin,end)
        
    data=cursor.query(sql).fetchall()
    c=Chart()
    c.type='column'
    c.yaxis_name='counts'
    c.data_list=["counts"]
    return c.generate(data, 'by db') 

    
def main():
    return
if __name__ == "__main__":
    main()