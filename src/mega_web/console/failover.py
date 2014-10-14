# -*- coding:utf-8 -*-
'''
Created on Sep 2, 2014

@author: xchliu

@module:mega_web.console.failover
'''
from lib.utils import now
from lib.PyMysql import PyMySQL
from apis.task import remote_cmd
from conf.GlobalConf import MSG_ERR_SERVER_EXITST,MSG_ERR_NAME
from mega_web.resource.instance_manage import InstanceGet

class FailoverManage():
    '''
    '''
    def __init__(self,request):
        self.q=PyMySQL()
        if request:
            self.name=request.get('name')
            self.type=request.get('type')
            self.wvip=request.get('wvip')
            self.rvip=request.get('rvip')
            self.master=request.get('master')
            self.manager=request.get('manager')
            self.id=request.get('id')        
        
    def _data_check(self):
        if not self.name:
            return False
        if not self.rvip:
            self.rvip=0
        return True
        
    def _check_ifexist(self):
        sql="select id from failover where name='%s'" % self.name
        id=self.q.fetchOne(sql)
        if id:
            return id
        return False
    
    def add_failover(self):
        if not self._data_check():
            return False,MSG_ERR_NAME
        if self._check_ifexist():
            return False,MSG_ERR_SERVER_EXITST
        sql="insert into failover(name,master,manager,rvip,wvip,type) values('%s',%s,%s,%s,%s,%s)" %(self.name,self.master,self.manager,self.rvip,self.wvip,self.type)
        print sql
        result,ex=self.q.execute(sql)
        if not result:
            return False,ex
        return True,''
    
    def mod_failover(self):
        if not self._data_check():
            return False,MSG_ERR_NAME
        id=self._check_ifexist()
        if not self.id or not id:
            return False,'NOT FOUND'
        if int(id)!=int(self.id):
            return False,MSG_ERR_SERVER_EXITST
        sql="update failover set name='%s',master=%s,manager=%s,rvip=%s,wvip=%s,type=%s where id=%s" %(self.name,self.master,self.manager,self.rvip,self.wvip,self.type,self.id)
        result,ex=self.q.execute(sql)
        if not result:
            return False,ex
        return True,''
    def change_master(self,failoverid,new_master,method):
        '''            
            usage: python mha_switch.py --group=xx --old_master=ip:port --new_master=ip:port --type=xx --record=xx
        '''
        cmd='mha_switch.py'
        cmd_type='python'
        sql='select s.name,s.ip,master from failover f ,server s where  f.manager=s.id and f.id=%s' %failoverid       
        (group,ip,old_master)=self.q.fetchRow(sql)
        #data=self.q.fetchRow(sql)
        _old=InstanceGet().get_instance_by_id(old_master)
        _new=InstanceGet().get_instance_by_id(new_master)
        _old_m="%s:%s" %(_old.get('ip'),_old.get('port'))
        _new_m="%s:%s" %(_new.get('ip'),_new.get('port'))
        record_id=self.add_failover_record(failoverid, method,_old_m,_new_m)
        self.add_failover_record_detail(record_id, 'mega',now(),0, 'Y', 'Start the switch task.')
        args="--group=%s --old_master= --new_master=%s:%s --type=%s --record=%s" %(group,_old_m,_new_m,method,record_id)
        #group name ,old master ,new master,action
        result=remote_cmd(ip,None,cmd,cmd_type,args)
        if result == 0:
            self.stat_failover_record(record_id, 'Failed')
            self.add_failover_record_detail(record_id, 'mega',now(),0, 'Y', 'End the task as failed to call remote script')
            return False
        else:
            self.add_failover_record_detail(record_id, 'mega',now(),0, 'Y', 'Call the remote script on %s' % ip)
            return True
            
    def add_failover_record(self,failover_id,method,old_master,new_master,failover_name=None):
        '''
            1.add a failover record with a given failover id  --used for mega web site
            2.add record with a failover group name  --used for command line ha switch
            
            return :
                None: failed to get the new record
                id(int): the new record for failover switch
        '''
        if not failover_id:
            if not failover_name:
                return None
            else:
                sql="select id from failover where name='%s'" % failover_name                
                failover_id=self.q.fetchOne(sql)
        sql="insert into failover_record (failover_id,method,re_time,old_master,new_master,result) values(%s,'%s',now(),'%s','%s','Running')"\
                                                                                 %(failover_id,method,old_master,new_master)
        result,ex=self.q.execute(sql)
        if result:
            record_id=self.q.fetchOne("select last_insert_id()")
        else:
            record_id=None
        return record_id
    
    def stat_failover_record(self,record_id,stat='Y'):
        '''
            1.stat the result for a switch task
            return ：
                True | False

        '''
        if not record_id:
            return None
        sql="update failover_record set result='%s' where id=%s" % (stat,record_id)
        result,ex= self.q.execute(sql)
        if not result :
            return False
        else:
            return True
    
    def add_failover_record_detail(self,record_id,module,re_time,time_used,result,content):
        '''
            record_id  ,get from the function add_failover_record()
            1.if task invoked by mega, the id will be given
            2.if task begins from the command line, call the add_failover_record() and get the new record id 
            befor add new detail logs
            return ：
                True | False
        '''
        if not record_id:
            return False        
        sql="insert into failover_record_detail(record_id,module,re_time,time_used,result,content) \
            values(%s,'%s','%s',%s,'%s','%s');" %(record_id,module,re_time,time_used,result,content)
        result,ex=self.q.execute(sql)
        if not result :
            return False
        else:
            return True
        
class FailoverGet():
    '''
    '''
    def __init__(self):
        self.q=PyMySQL()
        
    def get_failover_list(self,ip=None):
        
        sql='''select f.id as id,f.name as name,f.type as type,i.id as instance_id,concat(i.ip ,':',i.port) as master,s.id as server_id,s.ip as manager,v.id as rvip_id,v.vip as rvip,
            v2.id as wvip_id,v2.vip as wvip, f.last_time from failover f left join instance i on f.master=i.id  left join server s on f.manager=s.id left join vip v on f.rvip=v.id left join vip v2 on f.wvip=v2.id where 1=1 '''
        if ip :
            sql+="and v.vip='%s' or v2.vip='%s'" % (ip,ip)
        failover_list=self.q.query(sql, type='dict')
        return failover_list
    
    def get_failover_by_id(self,id):
        if not id:
            return None 
        sql="select a.name,concat(b.ip,':',b.port) as old_master,c.vip as rvip,d.vip as wvip from failover a left join  instance b on \
            a.master=b.id left join vip c on a.rvip=c.id left join vip d on a.wvip=d.id where a.id=%s;" % id
        return self.q.query(sql, type='dict').fetchone()

    def get_failover_history(self,id): 
        if not id:
            return None 
        sql="select * from failover_record where failover_id=%s order by id desc" %id
        return self.q.query(sql, type='dict').fetchall()
    
    def get_failover_history_detail(self,record_id,failover_id=None):
        if not record_id:
            if not failover_id:
                return None
            else:                
                record_id=self.get_newest_record(failover_id)
        sql="select * from failover_record_detail where record_id=%s order by id desc " %record_id
        return self.q.query(sql, type='dict').fetchall()

    def get_newest_record(self,failover_id):
        sql="select max(id) from failover_record where failover_id=%s" %failover_id
        return self.q.fetchOne(sql)

    def get_failover_result(self,record_id): 
        if not record_id:
            return {}
        sql="select result from failover_record where id=%s" %record_id
        return self.q.query(sql, type='dict').fetchone()
        
def main():
    return

if __name__ == "__main__":
    main()