# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_service.mega_client.upgrade
'''

from logs import Logger
from sender import MegaClient
from utils import get_ip_address

MODEL='Upgrade'
log = Logger(MODEL).log()

class Upgrade():
    
    def __init__(self):
        self.cmd='client_upgrade'
        self.c=MegaClient(cmd=self.cmd)
    
    def run(self):
        domain,ip=get_ip_address()
        ip="['"+ip+"']"      
        pag=self.c.run(func_args=ip,TOOL=True)
        pag=eval(pag)
        print pag
        f=open(pag[0],'wb')
        map(f.write,pag[1])
        f.close()
    
        
def main():
    Upgrade().run()

if __name__ == "__main__":
    main()