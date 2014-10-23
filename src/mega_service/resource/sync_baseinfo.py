# -*- coding:utf-8 -*-
'''
Created on Oct 17, 2014

@author: xchliu

@module:mega_service.resource.sync_baseinfo
'''

from lib.utils import now
from mega_web.resource.database_manage import DatabaseGet
from mega_web.resource.database_manage import DatabaseManage

from lib.logs import Logger

MODEL='Service-resource'
log=Logger(MODEL).log()

class SyncBasic():
    '''
        sync the instance basic infomation with the given data
            base=['variables','table_status','mysql_user','db_name','base']+['timestamp']+['except']
            state=['status','slave_status']+['timestamp']+['except']
        
        instance:"ip:port"
    '''
    
    def __init__(self,instanceid,instance=None,tag_time=None):
        self.instance_id=instanceid
        if instance:
            self.instance_ip,self.instance_port=instance.split(':')
        else:
            self.instance_ip=self.instance_port=''
        if tag_time:            
            self.tag_time=tag_time
        else:
            self.tag_time=now()
        self.q=PyMySQL()
    
    def sync_base(self,data,key):
        keys={'base':self.sync_instance,
              'status':self.sync_status,
              'variables':self.sync_variables,
              'table_status':self.sync_table_info,
              'mysql_user':self.sync_user_info,
              'db_name':self.sync_db_info,
              'slave_status':self.sync_slave_status
              }
        if key in keys:
            keys.get(key)(data)
        else:
            log.warn("unexpected key:%s .available keys:%s " % (key,[key for key in keys]))      
                           
    def sync_instance(self,data=None):
        '''
            'cnf': '/exportrvers/data/my3308/my.cnf'
            'version': u'5.6.16'
        '''
        if not data:
            return False      
        sql="update instance set version='%s',cnf_file='%s' where id=%s" %(data.get('version'),data.get('cnf'),self.instance_id) 
        self.q.execute(sql)       
        return True
    
    def sync_variables(self,data=None):
        '''
            sync the variables 
        '''
        for var in data:
            try:
                var_id=self.get_var_id(var)
                if var_id:
                    sql="insert variables_his(instance_id,variable_id,value,insert_time) values(%s,%s,'%s','%s')" \
                            % (self.instance_id,var_id,data.get(var,'null'),self.tag_time)
#                    log.debug(sql)
                    result,ex=self.q.execute(sql)
                    if not result:
                        log.error('Failed to save variable data as :%s' % ex)
            except Exception as ex:
                log.error("Save variables info failed :%s" % ex)
        
    def sync_table_info(self,data=None):
        '''
            sync the table status           
           {'ENGINE': 'InnoDB', 'TABLE_ROWS': '0', 'INDEX_LENGTH': '16384', 'DATA_LENGTH': '16384', 'db_name': 'dbchecksum', 'TABLE_NAME': '_dba_worksheet', 'TABLE_COMMENT': ''} 
        '''
        for table in data:
            try:
                table_name=table.get('table_name','')
                if not table_name:
                    continue
                #get database id
                db_name=table.get('db_name')                
                db=DatabaseGet().get_database_unique(self.instance_id,db_name)
                if db:
                    db_id=db[0].get('id')
                else:                
                    self.sync_db_info([db_name])
                    db=DatabaseGet().get_database_unique(self.instance_id, db_name)
                    if db:
                        db_id=db[0].get('id')
                    else:
                        db_id=0
                index_size=table.get('index_length',0)
                data_size=table.get('data_length',0)
                table_rows=table.get('table_rows',0)
                engine=table.get('engine','')            
                sql="insert into tables (instance_id,db_id,table_name,index_size,data_size,table_rows,engine,insert_time) \
                    values(%s,%s,'%s',%s,%s,%s,'%s','%s')" %(self.instance_id,db_id,table_name,index_size,data_size,table_rows,engine,self.tag_time)
                result,ex=self.q.execute(sql)
                if not result:
                    log.error(ex)
            except Exception as ex:
                log.error("Save table info failed :%s" % ex)
                
    def sync_user_info(self,data=None):
        '''
            sync the user info
            {'dbchecksum@172.17.62.45': "GRANT SELECT, INSERT, LOCK TABLES ON `dbchecksum`.* TO 'dbchecksum'@'172.17.62.45'",
             'zhanglei@172.17.62.38': "GRANT ALL PRIVILEGES ON *.* TO 'zhanglei'@'172.17.62.38'}             
        '''
        for user in data:
            _user,_host=user.split('@')
            try:
                sql='''insert mysql_user(instance_id,name,host,privilege,insert_time) values(%s,'%s','%s',"%s",'%s')''' \
                            % (self.instance_id,_user,_host,data.get(user,'null'),self.tag_time)
                #log.debug(sql)
                result,ex=self.q.execute(sql)
                if not result:
                    log.error('Failed to save user info as %s@%s:%s' % (_user,_host,ex))
            except Exception as ex:
                log.error("Save  user info failed :%s" % ex)        
        return
        
    def sync_db_info(self,data=None):
        '''
            sync the db info,add the database info if the db not found
            ['dbchecksum', 'dbchecksum_bak', 'mega', 'report']
        '''
        for db in data:
            try:
                db_id=DatabaseGet().get_database_unique(self.instance_id, db)
                if not db_id:
                    result,msg=DatabaseManage({"database_name":db,"database_ip":self.instance_ip,"database_port":self.instance_port}).add_database()
                    if result:
                        log.info("Add database : %s" % db)
                    else:
                        log.error("Failed to add database %s :%s" % (db,msg))
            except Exception as ex:
                log.error("Save db info failed :%s" % ex)
                    
    def sync_status(self,data=None):
        '''
            sync the status
        '''
        for status in data:
            try:
                status_id=self.get_status_id(status)
                if status_id:
                    sql="insert status_his(instance_id,status_id,value,insert_time) values(%s,%s,'%s','%s')" \
                            % (self.instance_id,status_id,data.get(status,'null'),self.tag_time)
                    result,ex=self.q.execute(sql)
                    if not result:
                        log.error('Failed to save variable data as :%s' % ex)
            except Exception as ex:
                log.error("Save  status info failed :%s" % ex)
    
    def sync_slave_status(self,data=None):
        '''
            sync the slave status
        '''
        for status in data: 
            try:
                sql="insert into slave_status(instance_id,name,value,insert_time) values(%s,'%s','%s','%s')" \
                    % (self.instance_id,status,data.get(status,'null',self.tag_time))
                result,ex=self.q.execute(sql)
                if not result:
                    log.error('Failed to save variable data as :%s' % ex)
            except Exception as ex:
                log.error("Save slave status info failed :%s" % ex)

    def get_var_id(self,var):
        if not var:
            return None
        var=var.lower()
        #func to get the variable id
        def _get_id():
            sql="select id from variables where name='%s';" % var
            var_id=self.q.fetchRow(sql)
            if var_id:
                return var_id[0]
            else:
                return None
        var_id=_get_id()
        #insert a new record if the variable does not exist
        if not var_id:
            sql="insert into variables(name) values('%s');" % var
            result,ex=self.q.execute(sql)
            if result:
                var_id=_get_id()
            else: 
                var_id=None               
                log.error('Get variable id failed:%s %s' % (var,ex))                
        return var_id

    def get_status_id(self,status):
        if not status:
            return None
        #func to get the status id
        def _get_id():
            sql="select id from status where name='%s';" % status
            status_id=self.q.fetchRow(sql)
            if status_id:
                return status_id[0]
            else:
                return None
        status_id=_get_id()
        #insert a new record if the variable does not exist
        if not status_id:
            sql="insert into status(name) values('%s');" % status
            result,ex=self.q.execute(sql)
            if result:
                status_id=_get_id()
            else: 
                status_id=None               
                log.error('Get variable id failed:%s %s' % (status,ex))                
        return status_id

        
        
def main():
    return
if __name__ == "__main__":
    main()