# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_client.mega_client.utils
'''
import socket
 
def get_ip_address():
    myname = socket.getfqdn(socket.gethostname(  ))
    myip = socket.gethostbyname(myname)
    return myname,myip

#print get_ip_address() 