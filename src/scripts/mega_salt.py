# coding: utf-8
#Created on 2014-06-12
#@author: gxg
#Usage:mega_salt use for doing db backup by mega calling 

import sys
sys.path.append('/export/servers/script/mega-master/src/mega_service/')
reload(sys)
sys.setdefaultencoding('utf8')

import salt.client
import json, traceback
import time
import os
import commands
import ast
import getpass

def saltcmdrun(ip,command,args):
    '''
    command 是命令脚本，调用远程服务器脚本(带绝对路径)
    '''
    #ip = ['172.17.62.43','172.17.62.42']
    client = salt.client.LocalClient()
    #res = client.cmd(ip, 'cmd.run',[command],timeout=86400,expr_form='list')
    #res = client.cmd(ip, 'cmd.script',[command],kwarg=args,timeout=86400,expr_form='list')
    res = client.cmd_async(ip, 'cmd.script',[command],timeout=86400,expr_form='list')
    return res

def backup_salt_client(args):
    ''''''
    feadback = {}
    ip_list = [ip["host_ip"] for ip in args]
    for ips in ip_list:
       result = saltcmdrun(ips,'salt:\\mega_db_backup.py',args)
       feadback[ips] = result
    return feadback


if __name__ == "__main__":
#*#    if len(sys.argv) !=1:
#*#        print "USAGE:\n", USAGE.strip("\n")
#*#        sys.exit(0)
#*#    args = sys.argv
    args =[ {'id'          : 1,
         'host_ip'     : '172.17.62.37',
         'port'        : 3309,
         'db_type'     : 'mysql',
         'backup_tool' : 'xtrabackup',
         'backup_level': 'instance',
         'level_value' : '',
         'backup_type' : 'full',
         'need_data'   : 'Y',
         'need_schema' : 'Y',
         'Iscompressed': 'Y',
         'isEncrypted' : 'Y',
         'retention'   : '7',
        },
       {'id'          : 1,
         'host_ip'     : '172.17.62.38',
         'port'        : 3309,
         'db_type'     : 'mysql',
         'backup_tool' : 'xtrabackup',
         'backup_level': 'instance',
         'level_value' : '',
         'backup_type' : 'full',
         'need_data'   : 'Y',
         'need_schema' : 'Y',
         'Iscompressed': 'Y',
         'isEncrypted' : 'Y',
         'retention'   : '7',
        }
       ]
    res = backup_salt_client(args)
    print json.dumps(res, indent = 4, sort_keys=True)
                  
