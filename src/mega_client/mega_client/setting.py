# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_service.mega_client.setting

'''

TCP_HOST=''  # default 0.0.0.0
TCP_PORT=1105
MAIL_HOST='172.17.58.25'


#all the script invoked by worker should be in the directory
SCRIPT_DIR='/home/mysql/admin/mega_client/script/'

#only used for client . 
CLIENT_DIR='/home/xdba/'

DEAFULT_LOG_DEBUG=True
LOG_FILE_NAME='/var/log/mega/mega_client.log'

DAEMON_PID='/var/run/mega_client.pid'
DAEMON_LOG=LOG_FILE_NAME

DEFAULT_TARGET='cmd'