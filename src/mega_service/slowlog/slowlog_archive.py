# -*- coding:utf-8 -*-
'''
Created on Aug 20, 2014

@author: xchliu

@module:mega_service.slowlog.slowlog_archive
'''
import time
from hashlib import md5
from lib.sql_parse import SQLParse
from lib.PyMysql import PyMySQL
from lib.utils import today
from lib.logs import Logger


MODEL='slowlog_statics'
log = Logger(MODEL).log()
#from mega_web.resource.instance_manage import InstanceGet

def slowlog_statics_per_hour(v_time):
    '''
        1.slowlog_archive_hour     
        2.slowlog_time_day
    '''
    #get the 
    _hour=v_time.split(':')[0]
    _pre_hour=int(_hour)-1
    _time="%s %s:00:00" % (today(),_hour)
    _pre_time="%s %s:00:00" % (today(),_pre_hour)
    _pre_time=int(time.mktime(time.strptime(_pre_time,'%Y-%m-%d %H:%M:%S')))
    _time=int(time.mktime(time.strptime(_time,'%Y-%m-%d %H:%M:%S')))
    sql_1='''insert into slowlog_sql_hour(hash_code,log_time,counts,max_time,avg_time,min_time,max_row,avg_row,min_row)
         select hash_code,from_unixtime(start_time),count(*),max(query_time),avg(query_time),min(query_time),max(rows_examined),avg(rows_examined),min(rows_examined) 
         from slowlog_info where start_time between '%s' and '%s' group by hash_code;''' %(_pre_time,_time)
    #log.debug(sql_1)
    result,ex=PyMySQL().execute(sql_1)
    if not result :
        log.error(ex)
   
    #
    sql_2="select instance_id,dbname,start_time,count(*) as counts from slowlog_info  where start_time between '%s' and '%s' group by instance_id,dbname;" \
            % (_pre_time,_time)
    #log.debug(sql_2)
    cursor=PyMySQL().query(sql_2, type='dict')
    data_list=cursor.fetchall()
    if data_list and len(data_list) >0 :
        _list=(1,5,10,100)
        for data in data_list:
            _counts=[]
            c=''
            for l in _list:
                _c=0
                _sql="select count(*) from slowlog_info where instance_id=%s and dbname='%s' and start_time between '%s' and '%s' and query_time<%s;" \
                        %(data.get('instance_id'),data.get('dbname'),_pre_time,_time,l)
                _c=PyMySQL().fetchOne(_sql)
                _counts.append(int(_c))
            _counts.append(int(data.get('counts')-sum(_counts)))
            #make sure all the values bigger than zero
            _counts=map(lambda x :abs(x),_counts)
            data['count_all']=_counts
            sql_3="select id from slowlog_time_day where instance_id=%s and db='%s' and date(log_time)='%s'" %(data.get('instance_id'),data.get('dbname'),today())
            #log.debug(sql_3)
            row_id=PyMySQL().fetchOne(sql_3)
            c=data.get('count_all')
            if not row_id or row_id == 0:
                _sql="insert into slowlog_time_day(instance_id,db,log_time,counts,lt_one,lt_five,lt_ten,lt_hundred,gt_hundred) values(%s,'%s',from_unixtime('%s'),%s,%s,%s,%s,%s,%s)" % (data.get('instance_id'), 
                                                                                                                                              data.get('dbname'),data.get('start_time'),
                                                                                                                                              data.get('counts'),c[0],c[1],c[2],c[3],c[4])
            else:
                _sql="update slowlog_time_day set counts=counts+%s,lt_one=lt_one+%s,lt_five=lt_five+%s,lt_ten=lt_ten+%s,lt_hundred=lt_hundred+%s,gt_hundred=gt_hundred+%s \
                     where id=%s" %(data.get('counts'),c[0],c[1],c[2],c[3],c[4],row_id) 
      #      log.debug(_sql)
            result,ex=PyMySQL().execute(_sql)
            if not result :
                log.error(ex)
    return True
        
def slowlog_pack(sql):

    sql_parsed=SQLParse(sql).var_replace()
    sql_hash=md5(sql_parsed.encode('utf8')).hexdigest()
    _sql="select count(*) from sql_format where hash_code='%s'" % sql_hash
    _counts=PyMySQL().fetchOne(_sql)
    if _counts == 0:
        _sql="insert into sql_format(hash_code,sql_parsed) values('%s','%s')" %(sql_hash,sql_parsed)
        PyMySQL().execute(_sql)
    return sql_hash

def main():
    return
if __name__ == "__main__":
    main()