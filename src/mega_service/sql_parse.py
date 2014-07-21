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
            if item.find('=') != -1:
                k,v=item.split('=')
                v='N'
                item="%s=%s" % (k,v)
            return item
        self._standard_format()
        self.sql=map(_replace,self.sql.split())
        return self._get_hash(self.sql),self.sql
    

    def _get_hash(self,str=''):
        if str:
            return hash(str(time.time())+str)
        else:
            return hash(time.time())
        
    def _single_query(self):
        pass
    
if __name__ == "__main__":
    #sql="select 1 where id=2"
    sql="select * from status where instance_id=633306 and  insert_time=\"2014-04-06 05:20:00\";"
    sql="SELECT /*!40001 SQL_NO_CACHE */ * FROM `slave`;"
    #sql="insert into status_name(Variable_name) select  distinct Variable_name from status;"
    sql="load data local infile '/home/mysql/joke.txt' into table joke fields terminated by ','  lines terminated by '\r';"
    s=SQLParse(sql)
    print s.var_replace()