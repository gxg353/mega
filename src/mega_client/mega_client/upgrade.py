# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_service.mega_client.upgrade
'''
import os
import commands
from logs import Logger
from sender import MegaClient
from utils import get_ip_address
from setting import CLIENT_DIR

MODEL='Upgrade'
log = Logger(MODEL).log()

class Upgrade():
    
    def __init__(self):
        self.cmd='client_upgrade'
        self.c=MegaClient(host='172.17.62.37',cmd=self.cmd)
        self.setup_path=''
        
    def _get_pag(self):
        log.info('Start mega client upgrade')
        domain,ip=get_ip_address()
        ip="['"+ip+"']"      
        pag=self.c.run(func_args=ip,TOOL=True)
        pag=eval(pag)
        tmp_dir=os.path.join('/tmp',pag.pop(0))
        self.setup_path=tmp_dir
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
        for p in pag:            
            #/mega_client/__init__.py
            file_name=p.items()[0][0].lstrip('/')
            file_content=p.items()[0][1]
            file_path=os.path.join(tmp_dir,'/'.join(file_name.split('/')[:-1]))
            if not os.path.isdir(file_path):
                os.makedirs(file_path)
            f=open(os.path.join(tmp_dir,file_name),'wb+')
            f.write(file_content)
        f.close()
        return True
    
    def run(self):
        if not self._get_pag():
            return False
        #install package
        cmd='cd %s && python %s/setup.py install' % (self.setup_path,self.setup_path)
        self._do_command(cmd, 'Update package')
                #restart the client server
        cmd='\\cp -ar %s %s' % (self.setup_path,CLIENT_DIR)
        self._do_command(cmd, 'replace client source')
        cmd='python /etc/init.d/mega_client restart'
        self._do_command(cmd, 'Restart mega client')
        
    def _do_command(self,cmd,action):
        _status,_output=commands.getstatusoutput(cmd)
        if _status <> 0:
            log.error('%s filed : %s' % (action,_output))
        else:
            log.info('%s success!' % action)

def main():
    Upgrade().run()

    
if __name__ == "__main__":
    main()