import os
#bool
DEV=True
DEBUG=True
#DEBUG=False
#log
DEAFULT_LOG_DEBUG=DEBUG
#Service
DEFAULT_TCP_PORT=1104
DEFAULT_TCP_HOST=''
TCP_HEADER={'HEAD':'MEGA'}

#default values
DEFAULT_OS='Linux'
DEFAULT_LEVEL=1
DEFAULT_OWNER=1
DEFAULT_DBTYPE='MySQL'
DEFAULT_HATYPE='MS'
DEFAULT_BUSINESS=1
DEFAULT_DB_PORT=3306
DEFAULT_PWD='123'
#STAT
STAT_ONLINE=1
STAT_OFFLINE=0
#TIME
DATETIME_FORMATE="%Y-%m-%d %H:%M:%S"

#API 
ERR_CODE_DEFAULT=None  #INIT CODE :Nonmeaning
ERR_CODE_UNKOWN=-1  #UNKONW
ERR_CODE_SUCCESS=0   #NO ERROR OCCUR
ERR_CODE_INVALID=2

#messages
MSG_ERR_IP='Invalid IP !'
MSG_ERR_PORT='Invalid PORT !'
MSG_ERR_LEVEL='Invalid LEVEL !'
MSG_ERR_NAME='Invalid NAME !'
MSG_ERR_INSTANCE_EXITST='Instance already exists !'
MSG_ERR_BUSINESS_EXITST='Business already exists !'
MSG_ERR_DB_EXITST='Database already exists !'
MSG_ERR_SERVER_EXITST='Server already exists !'

#backup
BACKUP_TOOL=['xtrabackup','mysqldump','mysqlbinlog','mydumper','rman','expdp','exp']
BACKUP_TYPE=['full','increment','binlog','archivelog']
BACKUP_LEVEL=['instance','db','table']
BACKUP_CYCLE=['day','week','month']

#meta data
OS=['Linux','Other']
LEVEL=[1,2,3]
DB_TYPE=['MySQL','Oracle','Other']
HA_TYPE=['MS','None']