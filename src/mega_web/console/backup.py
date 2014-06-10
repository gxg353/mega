from mega_web.entity.models import Backup_History_Info 
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
