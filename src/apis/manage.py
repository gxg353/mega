import types
from mega_service.backup import Backuper
from mega_service.slowlog.slow_log import SlowLog
from mega_service.slowlog.slowlog_archive import slowlog_pack,slowlog_statics_per_hour
from mega_service.task import Task
from mega_service.resource import sync_baseinfo,sync_stat
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
    while 1:
        try:
            conn=PyMySQL()
            cursor=conn.query(sql, type='dict')
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
                result,ex=conn.execute(_sql)
                if not result:
                    log.error(ex)
            conn.close()
        except Exception as ex:
                log.debug(data)
                log.error('Pack slow log failed:%s' % ex)
                break
    # do the hourly statics 
    try:
        slowlog_statics_per_hour(time)
    except Exception as ex:
        log.error('Statics slow log hourly failed:%s' % ex) 

def update_ha_info(new_master,old_master):
    '''
        switch the role inside a ha group
        master format:'1.1.1.1:3306' 
    '''
    log.info('swith master role from %s to %s' % (old_master,new_master))
    try:
        _new_host,_new_port=new_master.split(':')
        _old_host,_old_port=old_master.split(':')
        _new_instance_id=InstanceGet().get_instance_by_ip_port(_new_host, _new_port)
        _old_instance_id=InstanceGet().get_instance_by_ip_port(_old_host,_old_port)
        if not _old_instance_id: 
            log.error('Instance not found' % _old_instance_id )
            return False        
        if not  _new_instance_id:
            log.error('Instance not found' % _new_instance_id )
            return False        
        _new_instance_id=_new_instance_id[0].get('id')
        _old_instance_id=_old_instance_id[0].get('id') 
        _new_instance=InstanceGet().get_instance_by_id(_new_instance_id)
        #if the new master is master already,return false
        if _new_instance.get('role') == 1:
            log.warn("Instance %s is already master!" % new_master)
            return False
        if _new_instance.get('master_id') == _old_instance_id:
            #change the master id for the slaves
            sql="update instance set master_id=%s where master_id=%s" %(_new_instance_id,_old_instance_id)
            result,ex=PyMySQL().execute(sql)
            if not result:
                return False            
                log.error(ex)
            #change the old master stat
            sql="update instance set master_id=%s,role=2 where id=%s" %(_new_instance_id,_old_instance_id)
            result,ex=PyMySQL().execute(sql)
            if not result:
                return False            
                log.error(ex)
            #change the new master role
            sql="update instance set role=1 where id=%s" %(_new_instance_id)
            result,ex=PyMySQL().execute(sql)
            if not result:
                return False            
                log.error(ex)   
        else:
            log.error("%s 's master id is %s ,not %s" %(new_master,_new_instance.get('master_id'),_old_instance_id))                     
    except Exception as ex:        
        log.error('update ha info failed:%s' % ex)
        return False
    return True

def data_collect(time=None):
    '''
        collect the base info and performance data from all the online instance which data collect configuration is on
        type:
            base: collect the basic information for the instance  ,will be called one time per day
            stat: collect the status infomation 
    '''
    #
    type="base"
    result=[] 
    instance_list=[]
    if time:
        if int(time.split(":")[0]) == 0:
            type="stat"        
    filter={'i.stat':1,'i.data_collect':1}
    config_list=InstanceGet().get_instance_list(filter, 0)
    for conf in config_list:
        instance={"ip":conf.ip,
                  "port":conf.port,
                  "type":type                  
                  }
        instance_list.append(instance)
    if len(instance_list):
        log.debug(instance_list)
        script=Task().get_task_by_name('datacollect')
        for instance in instance_list:
            result.append(remote_cmd(instance['ip'],instance['port'],script,'python',args=instance))
    if result:
        log.debug(result)
    log.info("%s instance data collect task are invoked." % len(instance_list))    

def data_collect_save(data):
    '''
        parse the data collect from the client script,split the values by the keys
        
        keys:
            base=['variables','table_status','mysql_user','db_name','base']+['timestamp']+['except']
            state=['status','slave_status']+['timestamp']+['except']        
    '''
    # pre-check for safe and translate the str to a dict
    _keys=['variables','table_status','mysql_user','db_name','base','timestamp','except','status','slave_status']
    try:
        data=eval(str(data))
        if type(data) != types.DictionaryType:
            log.warn('Inexpectant data format as type of the data is %s' % type(data))
            return False        
        #get instance id
        instance=data.keys()[0]
        ip,port=instance.split(":")
        instance_id=InstanceGet().get_instance_by_ip_port(ip, port)
        if not instance_id:
            log.error('Failed to get instance id for %s:%s' % (ip,port))        
            return False    
        instance_id=instance_id[0]['id']
        instance_data=data.get(instance)
        #caught the exception return by the script
        script_except=instance_data.pop('except',None)
        if type(instance_data) != types.DictionaryType:
            log.error("Invalid data format for %s" % instance)
            return False
        if script_except:
            log.warn("Data collect on %s : %s" % (instance,script_except))
        #save the data into database 
        collect_time=instance_data.pop('timestamp',None)
        _sync=sync_baseinfo.SyncBasic(instance_id,instance,collect_time)
        for _k in _keys:            
            if instance_data.get(_k):
                _sync.sync_base(instance_data.pop(_k),_k)                
    except Exception as ex:
        log.error(ex)
        return False
    return True
    

    
def main():
    return

if __name__ == "__main__":
    main()       