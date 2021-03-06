# -*- coding:utf-8 -*-

SERVICE_NAME='mega'
TRACKER_LIFCYCLE=10
DAEMON_PID='/var/run/%s.pid' % SERVICE_NAME
DAEMON_LOG='/var/log/%s.log' % SERVICE_NAME
LOG_FILE_NAME=DAEMON_LOG


class DbConfig():
    def __init__(self):
        pass
    db_host='127.0.0.1'
    db_port=3306
    db_user='root'
    db_pwd=''
    db_db='mega'
    db_charset='utf8'

MEGA_SERVER="mega-server.d.chinabank.com.cn"    #mega 后台服务
EMAIL_SERVER="mega-email.d.chinabank.com.cn"    # mega 邮件服务器
SMS_SERVER="mega-sms.d.chinabank.com.cn"       #mega 短信服务器