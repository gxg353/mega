from mega_web.entity.models import Backup_History_Info 
from conf.GlobalConf import BACKUP_TOOL,BACKUP_TYPE,BACKUP_LEVEL,BACKUP_CYCLE
class Backup():
    def __init__(self):
        self.backup_info=Backup_History_Info
    def get_newest_backup_list(self):
        sql="select * from backup_history_info group by host_ip,port having(max(id));"
        return self.backup_info.objects.raw(sql)
    def get_config_by_instance(self,ip='',port=3306):
        if not port:
            port=3306
        sql="select * from backup_policy where host_ip='%s' and port=%s;" % (ip ,port)
        print sql
        return self.backup_info.objects.raw(sql)
    
class Backup_Config():
    def __init__(self):
        self.backup_tool=BACKUP_TOOL
        self.backup_type=BACKUP_TYPE
        self.backup_level=BACKUP_LEVEL
        self.backup_cycle=BACKUP_CYCLE