SERVICE_NAME='mega'
TRACKER_LIFCYCLE=10
SERVICE_PID_FILE='/tmp/%s.pid' % SERVICE_NAME
DAEMON_LOG='/var/log/%s.log' % SERVICE_NAME
class DbConfig():
    def __init__(self):
        pass
    db_host='127.0.0.1'
    db_port=3306
    db_user='root'
    db_pwd=''
    db_db='mega'
    db_charset='utf8'
