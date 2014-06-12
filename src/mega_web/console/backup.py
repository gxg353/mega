from mega_web.entity.models import Backup_History_Info,Backup_Policy
from conf.GlobalConf import BACKUP_TOOL,BACKUP_TYPE,BACKUP_LEVEL,BACKUP_CYCLE
from mega_web.resource.instance_manage import InstanceGet
class Backup():
    def __init__(self):
        self.backup_info=Backup_History_Info
    def get_newest_backup_list(self):
        sql="select * from backup_history_info group by host_ip,port having(max(id));"
        return self.backup_info.objects.raw(sql)
    def get_config_by_instance(self,ip='',port=3306):
        if not ip:
            return None,''
        if not port:
            port=3306

        instance_id=InstanceGet().get_instance_by_ip_port(ip, port)
        if not instance_id:
            instance_id=None
            return None,"Instance doest not exist!"
        else:
            sql="select * from backup_policy where host_ip='%s' and port=%s;" % (ip ,port)
            return self.backup_info.objects.raw(sql),''
    
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
            self.config_add()
        elif type == 'mod':
            self.config_mod()
        else:
            return False
    def config_add(self):
        self.backup_policy.host_ip=self.config.get("ip")
        self.backup_policy.port=self.config.get("port")
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
        return
    def config_mod(self):
        pass