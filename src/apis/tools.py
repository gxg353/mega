# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:apis.tools
'''
import os,sys
sys.path.append("..")
from lib.logs import Logger
from conf.settings import SERVICE_NAME,app_path
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
    pag_path=os.path.join(_prefix,'mega_client')
    try:
        _pag.append(pag_name)
        _pag.extend(read_file(pag_path,_prefix))
        return _pag
#        log.debug(f)
    except Exception as ex:
        log.error(ex)
    return ''

def read_file(path,prefix=''):
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

def main():
     client_upgrade()


if __name__ == "__main__":
    main()