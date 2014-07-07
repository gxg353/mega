import os,sys
#
app_path=os.path.dirname(sys.path[0])
SERVICE_NAME='mega'
TRACKER_LIFCYCLE=10
DAEMON_PID='/var/run/%s.pid' % SERVICE_NAME
DAEMON_LOG='/var/log/%s.log' % SERVICE_NAME
LOG_FILE_NAME=os.path.abspath('%s/log/mega.log' % app_path)

class DbConfig():
    def __init__(self):
        pass
    db_host='127.0.0.1'
    db_port=3306
    db_user='root'
    db_pwd=''
    db_db='mega'
    db_charset='utf8'
