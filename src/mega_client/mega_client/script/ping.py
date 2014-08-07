# -*- coding:utf-8 -*-
'''
Created on Aug 6, 2014

@author: xchliu

@module:mega_client.mega_client.script.ping
'''

from sender import MegaClient
from utils import get_ip_address
from setting import version

def main():
    '''
       keepalived check between mega service and client
    ''' 
    myname,myip=get_ip_address()
    
    cmd='client_ping'
    c=MegaClient(cmd=cmd)
    result=c.run(func_args="'%s',version='%s'" %(myip,version),TOOL=True)
    if result:
        return 'success'
    else:
        return 'failed'

if __name__ == "__main__":
    main()
