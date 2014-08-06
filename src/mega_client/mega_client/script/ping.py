# -*- coding:utf-8 -*-
'''
Created on Aug 6, 2014

@author: xchliu

@module:mega_client.mega_client.script.ping
'''

from mega_client.sender import MegaClient
from mega_client.utils import get_ip_address

def main():
    '''
       keepalived check between mega service and client
    ''' 
    myname,myip=get_ip_address()
    cmd='client_ping'
    c=MegaClient(cmd=cmd)
    result=c.run(func_args=myip,TOOL=True)
    if result:
        print 'success'
    else:
        print 'failed'

if __name__ == "__main__":
    main()
