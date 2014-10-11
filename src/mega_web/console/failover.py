# -*- coding:utf-8 -*-
'''
Created on Sep 2, 2014

@author: xchliu

@module:mega_web.console.failover
'''
from lib.PyMysql import PyMySQL
from apis.task import remote_cmd
from conf.GlobalConf import MSG_ERR_SERVER_EXITST,MSG_ERR_NAME
from mega_web.resource.instance_manage import InstanceGet

class FailoverManage():
    '''
    '''
    def __init__(self,request):
        self.q=PyMySQL()
        
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
            usage: python mha_switch.py --group=xx --old_master=ip:port --new_master=ip:port --type=xx
        '''
        cmd='mha_switch.py'
        cmd_type='python'
        sql='select s.name,s.ip,master from failover f ,server s where  f.manager=s.id and f.id=%s' %failoverid       
        (group,ip,old_master)=self.q.fetchRow(sql)
        #data=self.q.fetchRow(sql)
        _old=InstanceGet().get_instance_by_id(old_master)
        _new=InstanceGet().get_instance_by_id(new_master)
        args="--group=%s --old_master=%s:%s --new_master=%s:%s --type=%s" %(group,_old.get('ip'),_old.get('port'),_new.get('ip'),_new.get('port'),method)
        #group name ,old master ,new master,action
        result=remote_cmd(ip,None,cmd,cmd_type,args)
        if result == 0:
            return False
        else:
            return result
        
        
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

def main():
    return

if __name__ == "__main__":
    main()