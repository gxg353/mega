import types
from mega_service.backup import Backuper
from mega_service.slowlog.slow_log import SlowLog
from mega_service.slowlog.slowlog_archive import slowlog_pack,slowlog_statics_per_hour
from mega_service.task import Task
from mega_web.resource.instance_manage import InstanceGet
from lib.logs import Logger
from lib.PyMysql import PyMySQL
from task import remote_cmd

MODEL='API-manage'
log = Logger(MODEL).log()



def backup_routine(time=None,**args):
    instance_list=[]
    config_list=Backuper().backuper(time)
    for inst in config_list:
        inst_id=inst[0]
        inst_ip=inst[1]
        inst_port=inst[2]
        instance={
                  'id' : inst_id, 
                  'host_ip' : inst_ip, 
                  'port' : inst_port, 
                  'db_type' : inst[3], 
                  'backup_tool' : inst[4], 
                  'backup_level': inst[5], 
                  'level_value' : inst[6], 
                  'backup_type' : inst[7], 
                  'need_data' : inst[8], 
                  'need_schema' : inst[9], 
                  'Iscompressed': inst[10], 
                  'isEncrypted' : inst[11], 
                  'retention' : inst[12], 
                  } 
        instance_list.append(instance)
    len_inst=len(instance_list)
    result=[]
    if len_inst>0:
        script=Task().get_task_by_name('backup')
        for instance in instance_list:
            result.append(remote_cmd(instance['host_ip'],instance['port'],script,'python',args=instance))
    len_result=len(result)
    if result:
        log.debug(result)
    if len_inst >0:
        log.debug(instance_list)
        if len_inst==len_result :
            log.info("%s backup tasks are invoked.",len_inst)
        else:
            log.warn("%s backup tasks are invoked,%s are successed." %(len_inst,len_result))

def update_backupinfo(task_info,action='INSERT'):
    '''
        task_info : update items
        action: INSERT OR UPDATE 
    
    return :
        task id : insert or update success
        False :   unexpected errors occurs
    '''
    if not task_info :
        return False

    db_conn=PyMySQL()
    task=eval(str(task_info))
    if action.upper()=='INSERT':
        columns="host_ip,port,db_type,backup_tool,backup_level,level_value,backup_type,need_data,need_schema,status,rsync,message,backup_status,is_delete"
        values=[]
        data=(columns,)
        for c in columns.split(','):
            _d=task.get(c)
            if _d:
                values.append(_d)
            else:
                values.append('')
        data=data+tuple(values)
        sql="insert into backup_history_info(%s)\
            values('%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % data        
        db_conn.execute(sql)
        task_id=db_conn.fetchOne("select last_insert_id()")
        log.debug(sql)
        log.debug("New backup task id : %s  " %task_id)
        return task_id
    else:
        id=task.get("id")
        if not id:
            return False
        columns="status,is_delete,backup_begin_time,backup_end_time,rsync_begin_time,rsync_end_time,file_size,message,backup_status"
        values=[]
        data=""
        for c in columns.split(','):
            _d=task.get(c)
            if _d:
                data=data+c+" = '" + str(_d) + '\' ,'
        data=data.rstrip(',')
        sql="update backup_history_info set %s where id=%s" %(data,id)
        log.debug(sql)
        rows,msg=db_conn.execute(sql)   
        if rows or rows==0:
            if msg:
                log.debug(msg)
            return id
        else:
            log.warn("Update task %s : " % id +str(msg))
            return False
    return False

def add_slow_log(log_info):
    if not log_info:
        return False 
    db_conn=PyMySQL()
    if not db_conn:
        log.error('Failed connect to db server!')
        return False
    task=eval(str(log_info))
    log.debug(task)
    if type(task) != types.DictionaryType:
        log.error('Failed to revert slow log data to dict !')
        return False
    columns="db_host,port,start_time,user,user_host,Query_time,lock_time,Rows_sent,Rows_examined,sql_text,sql_explained,dbname"
    values=[]
    for c in columns.split(','):
        _d=task.get(c)
        if _d:
            _d='"'+str(_d)+'"'
            values.append(_d)
        else:
            values.append("''")
    #todo 
    #add proxy func    
    table_name='slowlog_info'
    sql="insert into %s(%s) values(%s)" %(table_name,columns,','.join(values))
    log.debug(sql)
    result,ex=db_conn.execute(sql)
    if result:
        task_id=db_conn.fetchOne("select last_insert_id()")
        log.debug('New slow log task id: %s' % task_id)
    else:
        task_id=0
        log.error(ex)
    return task_id

def slowlog_routine(time=None):
    instance_list=[]    
    config_list=SlowLog().get_slowlog_instance_list()
    log.debug(config_list)
    for conf in config_list:
        instance={"id":conf.get('id'),
                  "ip":conf.get('ip'),
                  "port":conf.get('port'),
                  "version":conf.get('version')
                  }
        instance_list.append(instance)
    inst_len=len(instance_list) 
    result=[]
    if inst_len>0:
        script=Task().get_task_by_name('slowlog')
        for instance in instance_list:
#            log.debug(instance)
            result.append(remote_cmd(instance['ip'],instance['port'],script,'python',args=instance))
    if inst_len >0:
        log.debug(instance_list)
    if result:
        log.debug(result)
    log.info('%s instance slow log collect tasks are invoked.' % inst_len)

def slowlog_statics(time=None):
    #get the slow log in the prior hour 
    #undo slow log
    sql="select * from slowlog_info where stat=0 limit 100" 
    try:
        while 1:
            cursor=PyMySQL().query(sql, type='dict')
            if not cursor:
                break
            data_list=cursor.fetchall()
            if not data_list or len(data_list)==0:
                log.warn('None slow log found!')
                break
            log.info('%s slow log will be computed.' % len(data_list))
            #add hash_code and instance to each log
            for data in data_list: 
                sql_hash=slowlog_pack(data.get('sql_text'))
                instance_id=InstanceGet().get_instance_by_ip_port(data.get('db_host'), data.get('port'))
                if not instance_id:
                    log.warn('Unknown Instance: %s' %([data.get('db_host'), data.get('port')]))
                    instance_id=0
                else:
                    instance_id=instance_id[0]['id']
                _sql="update slowlog_info set hash_code='%s',instance_id=%s,stat=1 where id = %s" %(sql_hash,instance_id,data.get('id'))
                result,ex=PyMySQL().execute(_sql)
                if not result:
                    log.error(ex)
    except Exception as ex:
                log.debug(data)
                log.error('Pack slow log failed:%s' % ex) 
        
    # do the hourly statics 
    try:
        slowlog_statics_per_hour(time)
    except Exception as ex:
        log.error('Statics slow log hourly failed:%s' % ex) 

def failover(group_name,old_master,new_master,method,time):
    '''
        1.update the instance and failover table ,change the replication relationship
        2.save the switch log
    '''
    return
    
    
def main():
    return

if __name__ == "__main__":
    main()       