# -*- coding:utf-8 -*-
'''
Created on Jul 16, 2014

@author: xchliu

@module:mega_service.slow_log
'''

import re
import time

class SQLParse():
    '''
        parse sql 
            replace the vars to N 
        return:
            sql after format and the hash string
            
    '''
    
    def __init__(self,sql):
        '''
        
        '''
        self.sql=sql
    KEY_ONE=[" SELECT "," FROM "," WHERE "," DESC "," ASC ",
             " DATE "," DAY "," INT "," CHAR "," VARCHAR "," DECIMAL ",
             " SUM "," AVG ","MAX","MIN"," COUNT "," AS "," TOP "," AND "," OR "]    
    KEY_TWO=[" GROUP BY "," ORDER BY "]
    SIGNS=['=','<','>','<>','!=']
        
    def _standard_format(self):
        sql=''
        _sql=self.sql
        #replace the space in '' or ""
        p=re.compile('(?:\'|")(.*?)(?:\'|")')
        mark=p.findall(_sql)
        for m in mark:
            _sql=_sql.replace(m,m.replace(' ','_')) 
            
        if _sql.find("'"):
            _sql=_sql.replace("'","")
        if _sql.find('"'):
            _sql=_sql.replace('"','')
        if _sql.find('"'):
            _sql=_sql.replace('"','')
        if _sql.find('\t'):
            _sql=_sql.replace('\t','')
        if _sql.find('\n'):
            _sql=_sql.replace('\n',' ')
        if _sql.find('`'):
            _sql=_sql.replace('`',' ')
        for _s in _sql.split():
            sql += _s + " "
        self.sql=sql
        
    def var_replace(self):
        if not self.sql:
            return False
        def _replace(item):
            for s in self.SIGNS:
                if item.find(s) != -1:
                    k,v=item.split(s)
                    v='N'
                    item="%s%s%s" % (k,s,v)
            return item
        self._standard_format()
        self.sql=' '.join(map(_replace,self._sign_format()))
        return self.sql
    
    def _sign_format(self):
        '''
            remove all the space between signs
        '''
        sql=self.sql.split()
        l=len(sql)
        for i in range(l):
            if sql[i] in self.SIGNS:                    
                if i==0 and l>0:
                    sql[i]=str(sql[i])+str(sql[i+1])
                    sql[i+1]=''
                elif i==-1:
                    sql[i]=str(sql[i-1])+str(sql[i])
                    sql[i-1]=''
                else:
                    sql[i]=str(sql[i-1])+str(sql[i])+str(sql[i+1])
                    sql[i+1]=''
                    sql[i-1]=''
        _new_sql=[x for x in sql if x]
        return _new_sql
        
    def _single_query(self):
        pass
    
if __name__ == "__main__":
    #sql="select 1 where id=2"
    sql="select * from status where instance_id=633306 and  insert_time=\"2014-04-06 05:20:00\";"
    sql="SELECT /*!40001 SQL_NO_CACHE */ * FROM `slave`;"
    #sql="insert into status_name(Variable_name) select  distinct Variable_name from status;"
    sql="load data local infile '/home/mysql/joke.txt' into table joke fields terminated by ','  lines terminated by '\r';"
    sql=" select count(*) COUNT  from (select a.dt as '\xe6\x97\xa5\xe6\x9c\x9f', a.ruletype as '\xe8\xa7\x84\xe5\x88\x99\xe7\xb1\xbb\xe5\x9e\x8b', a.ant as '\xe6\x8b\xa6\xe6\x88\xaa\xe4\xba\xa4\xe6\x98\x93\xe7\xac\x94\xe6\x95\xb0\xef\xbc\x88\xe7\xac\x94\xef\xbc\x89', format(100*a.ant/b.ant,2) as '\xe4\xba\xa4\xe6\x98\x93\xe7\xac\x94\xe6\x95\xb0\xe6\x8b\xa6\xe6\x88\xaa\xe7\x8e\x87\xef\xbc\x88%\xef\xbc\x89', format(a.amt,2) as '\xe6\x8b\xa6\xe6\x88\xaa\xe4\xba\xa4\xe6\x98\x93\xe9\x87\x91\xe9\xa2\x9d\xef\xbc\x88\xe5\x85\x83\xef\xbc\x89', format(100*a.amt/b.amt,2) as '\xe4\xba\xa4\xe6\x98\x93\xe9\x87\x91\xe9\xa2\x9d\xe6\x8b\xa6\xe6\x88\xaa\xe7\x8e\x87\xef\xbc\x88%\xef\xbc\x89' from ( select a1.dt,substring(a1.rule_no,1,1) as ruletype,count(a1.pay_no) as ant,sum(a1.tra_amt) as amt from (select dt,rule_no,pay_no,tra_amt from fct_dat_pay_order_risk_ctl_day Where substr(rule_no,1,1) not in('V','E','W') and length(rule_no)=10 and right(rule_no,1)<>'0'  and  dt='2014-07-18' and mer_no in('22792279','22809981') and biz_type='87')a1 left outer join (select pay_no from fct_dat_pay_order_risk_ctl_day Where substr(rule_no,1,1) ='E' and dt='2014-07-18')a2 on a1.pay_no=a2.pay_no where a2.pay_no is null group by a1.dt,ruletype )a left outer join ( select dt,count(pay_no) as ant,sum(tra_amt) as amt from fct_dat_pay_order_risk_ctl_day where dt='2014-07-18' and mer_no in('22792279','22809981') and biz_type='87' and (rule_no='' or rule_no='NULL') group by dt )b on a.dt=b.dt left outer join ( select c1.dt,substring(c1.rule_no,1,1) as ruletype,count(c1.pay_no) as ant,sum(c1.tra_amt) as amt from (select dt,rule_no,pay_no,tra_amt from fct_dat_pay_order_risk_ctl_day Where substr(rule_no,1,1) not in('V','E','W') and length(rule_no)=10 and right(rule_no,1)<>'0'  and  dt='2014-07-19' and mer_no in('22792279','22809981') and biz_type='87')c1 left outer join (select pay_no from fct_dat_pay_order_risk_ctl_day Where substr(rule_no,1,1) ='E' and dt='2014-07-19')c2 on c1.pay_no=c2.pay_no where c2.pay_no is null group by c1.dt,ruletype )c on a.ruletype=c.ruletype left outer join ( select dt,count(pay_no) as ant,sum(tra_amt) as amt from fct_dat_pay_order_risk_ctl_day where dt='2014-07-19' and mer_no in('22792279','22809981') and biz_type='87' and (rule_no='' or rule_no='NULL') group by dt ) d on c.dt=d.dt"
    sql="   select   SAMPLE_ID, BUSINESS_NAME, BUSINESS_SUBNO, BUSINESS_TYPE, SEND_NUM, ARRIVE_NUM, ARRIVE_TIME, SAMPLE_TIME  from sms_statistics_sample  where SAMPLE_TIME = '2014-08-25 14:43:00' and time='123' and id>10;"
    s=SQLParse(sql)
    print s.var_replace()