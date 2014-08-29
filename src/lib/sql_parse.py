# -*- coding:utf-8 -*-
'''
Created on Jul 16, 2014

@author: xchliu

@module:mega_service.slow_log
'''

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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
        if _sql.find(','):
            _sql=_sql.replace(',',', ')
        for _s in _sql.split():
            sql += _s + " "
        self.sql=sql
        
    def var_replace(self):
        if not self.sql:
            return False
        def _replace(item):
            print item
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
    sql="update client set heartbeat=now(),version='mega-client 0.1' where server_id=86;"
    sql="select count(*) COUNT  from (select concat(substring(a.dt,1,4),'/',substring(a.dt,5,2),'/',substring(a.dt,7,2))   as '\xe6\x97\xa5\xe6\x9c\x9f' ,concat(substring(a.tra_tm ,1,2),':',substring(a.tra_tm ,3,2),':',substring(a.tra_tm,5,2))   as '\xe4\xba\xa4\xe6\x98\x93\xe6\x97\xb6\xe9\x97\xb4' ,c.mer_nm   as '\xe5\x95\x86\xe6\x88\xb7\xe5\x90\x8d\xe7\xa7\xb0' ,a.rule_no as '\xe8\xa7\x84\xe5\x88\x99\xe7\xbc\x96\xe5\x8f\xb7' ,b.rule_desc  as '\xe8\xa7\x84\xe5\x88\x99\xe6\x8f\x8f\xe8\xbf\xb0' ,d.mer_order_no   as '\xe6\x94\xaf\xe4\xbb\x98\xe5\x8d\x95\xe5\x8f\xb7' ,a.bank  as '\xe9\x93\xb6\xe8\xa1\x8c' ,a.card_no  as '\xe9\x93\xb6\xe8\xa1\x8c\xe5\x8d\xa1\xe5\x8f\xb7' ,format(a.amt,2)   as '\xe9\x87\x91\xe9\xa2\x9d' ,case when tra_type='01' then '\xe6\xb6\x88\xe8\xb4\xb9' when tra_type='07' then '\xe9\x80\x80\xe6\xac\xbe'  else tra_type end as '\xe4\xba\xa4\xe6\x98\x93\xe7\xb1\xbb\xe5\x9e\x8b' ,a.tra_rslt  as '\xe4\xba\xa4\xe6\x98\x93\xe7\xbb\x93\xe6\x9e\x9c' ,case when a.is_stl=1 then '\xe6\x98\xaf' else '\xe5\x90\xa6' end as '\xe6\x98\xaf\xe5\x90\xa6\xe7\xbb\x93\xe7\xae\x97' from dm.fct_rpd_fast_pay_rule_detl_day a inner join dm.d99_moto_kuaijie_wg_rule b on a.rule_no = b.rule_cd left outer join (select * from FCT_DAT_MOTO_SP_DAY where pt='2014-08-24')c on a.mer_no=c.moto_mer_no left outer join (select * from FCT_DAT_MOTO_SP_PAY_DAY where pt='2014-08-24')d on a.tra_no=d.moto_pay_no where a.pt='2014-08-24' and a.rule_no='10'  and a.rule_no in ('8','9','10')) d_report_limit;"
    sql="select case when trim(ID) is null then '' else trim(ID) end,case when replace(replace(replace(MHT_ORDER_NO,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(MHT_ORDER_NO,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(FD_ORDER_NO,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(FD_ORDER_NO,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(CUST_ACC_NO,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(CUST_ACC_NO,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(ORDER_NO,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(ORDER_NO,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(MHT_CODE,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(MHT_CODE,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(FUND_CODE,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(FUND_CODE,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when trim(ORDER_AMT) is null then '' else trim(ORDER_AMT) end,case when replace(replace(replace(ORDER_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(ORDER_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when trim(ORDER_TIME) is null then '' else trim(ORDER_TIME) end,case when trim(TRADE_VOL) is null then '' else trim(TRADE_VOL) end,case when trim(BIZ_DATE) is null then '' else trim(BIZ_DATE) end,case when trim(SETTlE_DATE) is null then '' else trim(SETTlE_DATE) end,case when replace(replace(replace(IS_SPEED_ORDER,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(IS_SPEED_ORDER,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(RECON_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(RECON_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(SETTLE_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(SETTLE_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(IS_FROZEN,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(IS_FROZEN,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(TRADE_ERROR,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(TRADE_ERROR,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(RECON_ERROR,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(RECON_ERROR,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(FROZEN_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(FROZEN_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when replace(replace(replace(BORROW_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') is null then '' else replace(replace(replace(BORROW_STATUS,CHAR(9),' '),CHAR(10),' '),CHAR(13),' ') end,case when trim(CREATE_TIME) is null then '' else trim(CREATE_TIME) end,case when trim(LAST_UPDATE_TIME) is null then '' else trim(LAST_UPDATE_TIME) end,case when trim(PAYMENT_TIME) is null then '' else trim(PAYMENT_TIME) end, str_to_date('2014-08-27', '%Y-%m-%d') from funddb1.FD_REDEMPTION_ORDER t1 where date (t1.create_time) = '2014-08-27' or date (t1.last_update_time) = '2014-08-27';"
    s=SQLParse(sql)
    print s.var_replace()