from mega_service.backup import Backuper
from lib.logs import Logger
from mega_service.task import Task
from lib.PyMysql import PyMySQL
from scripts.mega_salt import backup_salt_client as mega_salt
MODEL='API-manage'
log = Logger(MODEL).log()


def backup_routine(task_id,**args):
    instance_list=[]
    config_list=Backuper().backuper()
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
    if len(instance_list)>0:
        result=mega_salt(instance_list)
#    result=[]
    if result:
        log.debug(result)
    if len(instance_list) >0:
        log.debug(instance_list)
        if len(instance_list)==len(result) :
            log.info("%s backup tasks are invoked.",len(instance_list))
        else:
            log.warn("%s backup tasks are invoked,%s are successed." %(len(instance_list),len(result)))
    Task().stat_task_by_id(task_id)

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
        columns="host_ip,port,db_type,backup_tool,backup_level,level_value,backup_type,need_data,need_schema,status,rsync,message"
        values=[]
        data=(columns,)
        for c in columns.split(','):
            _d=task.get(c)
            values.append(_d)
        data=data+tuple(values)
        sql="insert into backup_history_info(%s)\
            values('%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % data        
        log.debug(sql)
        db_conn.execute(sql)
        task_id=db_conn.fetchOne("select last_insert_id()")        
        log.debug("New backup task id : %s  " %task_id)
        return task_id
    else:
        id=task.get("id")
        if not id:
            return False
        columns="status,is_delete,backup_begin_time,backup_end_time,rsync_begin_time,rsync_end_time,file_size,message"
        values=[]
        data=""
        for c in columns.split(','):
            _d=task.get(c)
            data=data+c+" = '" + _d + '\' ,'
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
    
    
    