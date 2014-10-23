# -*- coding:utf-8 -*-
'''
Created on Oct 21, 2014

@author: xchliu

@module:tests.sync_base
'''
from mega_client import sender

data_stat={'172.17.62.56:3306':
            {
             'status': {'com_drop_function': '123', 'performance_schema_socket_instances_lost': '0'},
             'timestamp':'2014-10-21 10:52:23',
             'except':{},
             'slave_status':{}
            }
           }
data_base={'172.17.62.56:3306':
           {
            'timestamp':'2014-10-21 10:52:23',
            'variables':{'report_port': '3308', 'ignore_builtin_innodb': 'OFF', 'innodb_large_prefix': 'OFF', 'innodb_online_alter_log_max_size': '134217728'},
            'except':{'test':'test except'}, 
            'mysql_user':{'test@test1':'test','dbchecksum@172.17.62.45': "aaaGRANT SELECT, INSERT, LOCK TABLES ON `dbchecksum`.* TO 'dbchecksum'@'172.17.62.45'",}, 
            'db_name':['dbchecksum', 'dbchecksum_bak', 'mega', 'report'], 
            'base':{'cnf': '/export/servers/data/my3308/my.cnf', 'version': '5.6.16'},
            'table_status':[{'engine': 'InnoDB', 'table_rows': '0', 'index_length': '16384', 'data_length': '16384', 'db_name': 'mega_local', 'table_name': '_dba_worksheet', 'table_comment': ''}]            
            }           
           }
cmd='data_collect_save'
c=sender.MegaClient(cmd=cmd)
#r=c.run(func_args=data_stat)
#print "test data stat:%s" % r
r=c.run(func_args=data_base)
c.close()    
print "test data base:%s" % r

def main():
    return
if __name__ == "__main__":
    main()