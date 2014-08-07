# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:apis.tools
'''
import os,sys
sys.path.append("..")

from lib.PyMysql import PyMySQL
from lib.logs import Logger
from conf.settings import SERVICE_NAME,app_path
from mega_web.resource.server_manage import ServerGet
import release

MODEL='API-tool'
log = Logger(MODEL).log()


def client_upgrade(host_list=None):
    
    '''
        client upgrade for the given host list
    '''
    _pag=[]
    log.debug('Receive upgrade request: %s ' % host_list)
    version=release.version
    pag_name=SERVICE_NAME+"-"+version
    _prefix=os.path.join(app_path,'mega_client/dist',pag_name)
    #pag_path=os.path.join(_prefix,'mega_client')
    try:
        _pag.append(pag_name)
        _pag.extend(_read_file(_prefix,_prefix))
        return _pag
#        log.debug(f)
    except Exception as ex:
        log.error(ex)
    return ''

def _read_file(path,prefix=''):
    '''
        return a list contains all the file content in the given path 
    '''
    if not os.path.isdir(path):
        return []
    data=[]
    for root,dirs,files in os.walk(path):
        for file in files:
            file=os.path.join(root,file)       
            _f=open(file,'rb').read()
            _p=file.replace(prefix,'')
            data.append({_p:_f})
    return data

def client_ping(ip,version=None,**args):
    server_id=ServerGet().get_server_by_ip(ip)
    if not server_id:
        log.error("Get server id failed for %s" % ip)
    server_id=server_id[0]['id']
    sql="select count(*) from client where server_id=%s" % server_id
    _counts=PyMySQL().fetchOne(sql)
    if _counts == 0:
        sql="insert into client(server_id,version,heartbeat) values(%s,now())" % (server_id,version)
    else:
        sql="update client set heartbeat=now(),version='%s' where server_id=%s " %(version,server_id)
    result,ex=PyMySQL().execute(sql)
    if not result:
        log.error("Client keepalived check failed: %s %s" %(ip,ex))
        return ''
    return result
    
def main():
    print client_upgrade()


if __name__ == "__main__":
    main()