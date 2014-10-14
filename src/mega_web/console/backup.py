import time
import datetime
from lib.utils import today
from lib.PyMysql import PyMySQL
from mega_web.resource.server_manage import ServerGet
from mega_web.resource.instance_manage import InstanceGet
from mega_web.resource.business_manage import BusinessGet
from mega_web.entity.models import Backup_History_Info,Backup_Policy
from conf.GlobalConf import BACKUP_TOOL,BACKUP_TYPE,BACKUP_LEVEL,BACKUP_CYCLE,DEFAULT_DB_PORT,MIN_BACKUP_PERIOD



class Backup():
    def __init__(self):
        self.backup_info=Backup_History_Info
        self.backup_policy=Backup_Policy
        self.q=PyMySQL()
        
    def get_newest_backup_list(self,ip=None):
        if (not ip) or (ip == ''):
            sql="select * from backup_history_info order by id desc limit 150;"
        else:
            sql="select * from backup_history_info where host_ip='%s' limit 150;" % ip
        _data=[dict(d.__dict__) for d in self.backup_info.objects.raw(sql)]
        for _d in _data:
            ip=_d['host_ip']
            port=_d['port']
            instance_id=InstanceGet().get_instance_by_ip_port(ip, port)
            if not instance_id:
                continue
            instance_id=instance_id[0]['id']
            _d['instance_id']=instance_id
            inst=InstanceGet().get_instance_by_id(instance_id)
            _d['instance_name']=inst['name']
            _d['business_name']=BusinessGet().get_business_by_id(inst['business_id'])['name']
            _d['server_name']=ServerGet().get_server_by_id(inst['server_id'])['name']
        return _data
            
    def get_config_by_instance(self,ip='',port=3306):
        if not ip:
            return None,''
        if not port:
            port=3306
        instance_id=InstanceGet().get_instance_by_ip_port(ip, port)
        if not instance_id:
            instance_id=None
            return None,"Instance does not exist!"
        else:
            sql="select * from backup_policy where host_ip='%s' and port=%s;" % (ip ,port)
            return self.backup_info.objects.raw(sql),''
    def get_config_list(self,ip=None):
        if not ip :
            sql="select * from backup_policy order by is_schedule desc;"
        else:
            sql="select * from backup_policy where host_ip='%s';" % ip
        return self.backup_policy.objects.raw(sql)
    def get_today_statics(self,date=None): 
        if not date:
            date=today()               
        #planed counts
        _now={}
        _now["week"]=time.strftime('%a',time.strptime(date,'%Y-%m-%d'))
        _now["month"]=time.strftime('%d',time.strptime(date,'%Y-%m-%d'))        
        sql="select count(*) from backup_policy where cycle='day' and is_schedule=1"
        count_day=self.q.fetchOne(sql)
        sql="select count(*) from backup_policy where cycle='week' and find_in_set('%s',backup_time) and is_schedule=1" %(_now['week'])
        count_week=self.q.fetchOne(sql)
        sql="select count(*) from backup_policy where cycle='month' and find_in_set('%s',backup_time) and is_schedule=1" %(_now['month'])
        count_month=self.q.fetchOne(sql)
        total_today=count_day+count_week+count_month
        
        #ran backup
        sql="select count(*) from backup_history_info where date(backup_begin_time)='%s' and backup_status='Y' " % date
        success_count=self.q.fetchOne(sql)
        sql="select count(*) from backup_history_info where date(backup_begin_time)='%s' and backup_status='N' " % date
        failure_count=self.q.fetchOne(sql)
        success_ratio=(success_count*100)/total_today
        failure_ratio=(failure_count*100)/total_today
        return {"total_today":total_today,"success_count":success_count,"success_ratio":success_ratio,"failure_count":failure_count,"failure_ratio":failure_ratio}
   
    def get_uninvoked_backup(self,date=None):
        if not date:
            date=today()
        _now={}
        _now["week"]=time.strftime('%a',time.strptime(date,'%Y-%m-%d'))
        _now["month"]=time.strftime('%d',time.strptime(date,'%Y-%m-%d'))
        sql="select a.* from backup_policy a left join backup_history_info b  on a.host_ip=b.host_ip and a.port=b.port and a.backup_tool=b.backup_tool and \
            a.backup_level=b.backup_level and date(b.backup_begin_time)='%s' where a.cycle='day' and a.is_schedule=1  and  b.id is null;" %(date)
        _day=self.q.fetchAll(sql)
        sql="select a.*,b.id from backup_policy a left join backup_history_info b  on a.host_ip=b.host_ip and a.port=b.port and a.backup_tool=b.backup_tool \
             and a.backup_level=b.backup_level and date(b.backup_begin_time)='%s' where a.cycle='week' and a.is_schedule=1 and find_in_set('%s',backup_time)\
               and  b.id is null;" %(date,_now['week'])
        _week=self.q.fetchAll(sql)
        sql="select a.*,b.id from backup_policy a left join backup_history_info b  on a.host_ip=b.host_ip and a.port=b.port and a.backup_tool=b.backup_tool \
             and a.backup_level=b.backup_level and date(b.backup_begin_time)='%s' where a.cycle='month' and a.is_schedule=1 and find_in_set('%s',backup_time)\
               and  b.id is null;" %(date,_now['month'])
        _month=self.q.fetchAll(sql)
        data=[x for x in _day]+[x for x in _week]+[x for x in _month]
        return data
    
    def get_failed_backup(self,time=None):
        '''
            return the failed backup info in the given  or current hour 
        '''
        date=today()
        if not time:
            time=datetime.datetime.now().strftime('%H:%M')
        hour,minite=time.split(':')
        sql="select id,host_ip,port,db_type,backup_tool,backup_type,backup_begin_time,file_size,status,message from backup_history_info where \
            date(backup_begin_time)='%s' and hour(backup_begin_time)=%s and backup_status ='N';" %(date,hour)
        return self.q.fetchAll(sql)
    
    def get_unavailable_backup(self,time=None):
        '''
            return the list of instance which have no available backup in option days
        '''
        date=today(MIN_BACKUP_PERIOD)
        sql="select a.* from backup_policy a left join backup_history_info b  on a.host_ip=b.host_ip and a.port=b.port and a.backup_tool=b.backup_tool and \
            a.backup_level=b.backup_level and date(b.backup_begin_time)>'%s' where  a.is_schedule=1  and  b.id is null;" %(date)
        data=self.q.fetchAll(sql)
        return data
    
    
class Backup_Config():
    def __init__(self):
        self.backup_tool=BACKUP_TOOL
        self.backup_type=BACKUP_TYPE
        self.backup_level=BACKUP_LEVEL
        self.backup_cycle=BACKUP_CYCLE
        self.backup_policy=Backup_Policy()
    def config_deliver(self,config):
        self.config=config
        type=config.get('type')
        if type == 'add':
            return self.config_add()
        elif type == 'mod':
            return self.config_mod()
        else:
            return False
    def config_add(self):
        self.backup_policy.host_ip=self.config.get("ip")
        if self.config.get("port"):
            self.backup_policy.port=self.config.get("port")
        else:
            self.backup_policy.port=DEFAULT_DB_PORT
        if self.config.get("is_scheduled")=='ON':
            self.backup_policy.is_schedule=1
        else:
            self.backup_policy.is_schedule=0
        db_type=self.config.get("db_type")
        if not db_type:
            self.backup_policy.db_type='mysql'
        else:
            self.backup_policy.db_type=db_type
        self.backup_policy.backup_tool=self.config.get("backup_tool")
        self.backup_policy.backup_type=self.config.get("backup_type")
        self.backup_policy.isencrypted=self.config.get("isencrypted")
        self.backup_policy.cycle=self.config.get('backup_cycle')
        self.backup_policy.schedule_time=self.config.get("schedule_time")
        self.backup_policy.iscompressed=self.config.get("iscompressed")
        self.backup_policy.need_data=self.config.get("need_data")
        self.backup_policy.need_schema=self.config.get("need_schema")
        self.backup_policy.backup_level=self.config.get("backup_level")
        self.backup_policy.level_value=self.config.get("level_value")
        self.backup_policy.backup_time=self.config.get("backup_time")
        self.backup_policy.retention=self.config.get("retention")
        self.backup_policy.save()
        return True
    def config_mod(self):
        config_id=self.config.get("id")
        if config_id:
            backup_policy=Backup_Policy.objects.get(id=config_id)
        else:
            return False
        if self.config.get("is_scheduled")=='ON':
            self.backup_policy.is_schedule=1
        else:
            self.backup_policy.is_schedule=0
#        _time=time.strftime(self.config.get("schedule_time").replace('.',''),"%I:%M %p")
        
        backup_policy.backup_tool=self.config.get("backup_tool")
        backup_policy.backup_type=self.config.get("backup_type")
        backup_policy.isencrypted=self.config.get("isencrypted")
        backup_policy.cycle=self.config.get('backup_cycle')
        backup_policy.schedule_time=self.config.get("schedule_time")
        backup_policy.iscompressed=self.config.get("iscompressed")
        backup_policy.need_data=self.config.get("need_data")
        backup_policy.need_schema=self.config.get("need_schema")
        backup_policy.backup_level=self.config.get("backup_level")
        backup_policy.level_value=self.config.get("level_value")
        backup_policy.backup_time=self.config.get("backup_time")
        backup_policy.retention=self.config.get("retention")
        backup_policy.save()
        return True
        