from mega_service.backup import Backuper


def backup_routine(tasks,**args):
    instance_list=Backuper().backuper()
    for inst in instance_list:
        inst_id=inst[0]
        inst_ip=inst[1]
        inst_port=inst[2]
    print instance_list
    
#(18L, u'172.17.62.56', 3306L, u'mysql', u'xtrabackup', u'instance', u'123', u'full', u'Y', u'Y', u'Y', u'Y', 2L, 1L, u'week', u'Mon,Tue', u'17:37', datetime.datetime(2014, 6, 16, 17, 37, 4)),