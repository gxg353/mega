# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_client.mega_client.utils
'''
import socket as S
from socket import socket,SOCK_DGRAM,AF_INET

def get_ip_address():
    myname=''
    myip=''
    try:
        myname = S.getfqdn(S.gethostname())
        myip = S.gethostbyname(myname)
    except:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        myip=s.getsockname()[0] 
    return myname,myip

