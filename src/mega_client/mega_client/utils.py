# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_client.mega_client.utils
'''
import socket
 
def get_ip_address():
    myname=''
    myip=''
    try:
        myname = socket.getfqdn(socket.gethostname())
        myip = socket.gethostbyname(myname)
    except Exception as ex:
        from socket import socket, SOCK_DGRAM, AF_INET
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('google.com', 0))
        myip=s.getsockname()[0] 
    return myname,myip

#print get_ip_address() 