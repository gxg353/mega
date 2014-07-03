from mega_web.entity.models import Backup_History_Info,Backup_Policy
from conf.GlobalConf import BACKUP_TOOL,BACKUP_TYPE,BACKUP_LEVEL,BACKUP_CYCLE,DEFAULT_DB_PORT
from mega_web.resource.instance_manage import InstanceGet

class Backup():
    def __init__(self):
        self.backup_info=Backup_History_Info
        self.backup_policy=Backup_Policy

    def get_newest_backup_list(self,ip=None):
        if (not ip) or (ip == ''):
            sql="select * from backup_history_info group by host_ip,port having(max(id));"
        else:
            sql="select * from backup_history_info where host_ip='%s';" % ip 
        return self.backup_info.objects.raw(sql)
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
            sql="select * from backup_policy"
        else:
            sql="select * from backup_policy where host_ip='%s';" % ip
        return self.backup_policy.objects.raw(sql)
    
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
        