# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_service.mega_client.upgrade
'''
import os
import commands
from mega_client.logs import Logger
from mega_client.sender import MegaClient
from mega_client.utils import get_ip_address
from mega_client.setting import CLIENT_DIR,MEGA_HOST

MODEL='Upgrade'
log = Logger(MODEL).log()

class Upgrade():
    
    def __init__(self):
        self.mega_server=MEGA_HOST
        self.cmd='client_upgrade'        
        self.c=MegaClient(host=self.mega_server,cmd=self.cmd)
        self.setup_path=''
        
    def _get_pag(self):
        log.info('Start mega client upgrade')
        domain,ip=get_ip_address()
        ip="['"+ip+"']"      
        pag=self.c.run(func_args=ip,TOOL=True)
        if pag==0:
            log.error('Failed to connect to mega server:%s' % self.mega_server)
            return False
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
        os.chdir(self.setup_path)
        cmd=(
             ['Remove old package','cat %s/record.info| xargs rm -rf' % CLIENT_DIR ],
             ['Update package','python %s/setup.py install' %self.setup_path],
             ['Replace client source','cp -ar %s %s' % (self.setup_path,CLIENT_DIR)],
             ['Change file mod','chmod a+x /etc/init.d/mega_client'],
             ['Stop mega client','python /etc/init.d/mega_client upgrade']
             )
        for c in cmd:
            result=self._do_command(c[1],c[0])
            if not result:
                log.error('Abort upgrade!')
                break

    def _do_command(self,cmd,action):
        _status,_output=commands.getstatusoutput(cmd)
        if _status <> 0:
            log.error('%s failed : %s' % (action,_output))
            return False
        else:
            log.info('%s success!:%s' % (action,_output))
            return True


    
    
    
def main():
    Upgrade().run()
    
if __name__ == "__main__":     
    main()