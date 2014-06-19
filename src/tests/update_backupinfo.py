import sys
sys.path.append("..")
from mega_service.sender import MegaClient

var='''task_info={ "backup_tool": "xtrabackup", 
"backup_type": "full",
"db_type":"mysql",
"backup_level":"instance",
"level_value":"",
"need_data":"Y",
"need_schema":"Y",
"rsync":"Y",
"message": "xtrabackup is running now!", 
"host_ip": "172.17.62.37", 
"id": 1, 
"isEncrypted": "Y", 
"iscompress": "Y", 
"port": 3309, 
"retention": "7", 
"status": 1},action='insert'
'''
var_update='''task_info={"id":82,
"status": 'Y',
"is_delete":'Y',
"backup_begin_time":'2013:01:01 02:02:02',
"backup_end_time":'2013:01:01 02:02:02',
"rsync_begin_time":'2013:01:01 02:02:02',
"rsync_end_time":'2013:01:01 02:02:02',
'file_size':'2013:01:01 02:02:02',
'message':'test update'},action='update'
'''

def test_insert():
    cmd='update_backupinfo'
    c=MegaClient(cmd=cmd)
    print c.run(var)
def test_update():
    cmd='update_backupinfo'
    c=MegaClient(cmd=cmd)
    print c.run(var_update)




if __name__=="__main__":
    test_insert()
    test_update()