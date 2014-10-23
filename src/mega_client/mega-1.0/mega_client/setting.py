# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_service.mega_client.setting

'''
#meta data
version='mega-client 0.1'
TCP_HOST=''  # default 0.0.0.0
TCP_PORT=1105
MEGA_HOST='mega-server.d.chinabank.com.cn'
MEGA_HOST='localhost'


KEEPALIVE=300

#all the script invoked by worker should be in the directory
SCRIPT_DIR='/home/mysql/admin/mega_client/script/'

#only used for client . 
CLIENT_DIR='/home/mysql/'

DEAFULT_LOG_DEBUG=True
LOG_FILE_NAME='/var/log/mega/mega_client.log'
DAEMON_PID='/var/run/mega_client.pid'
SERVICE_PID='/var/run/mega_client_srv.pid'
DAEMON_LOG=LOG_FILE_NAME

DEFAULT_TARGET='cmd'

