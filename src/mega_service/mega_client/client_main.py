# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_service.mega_client.client_main
'''
import datetime
from listener import tcp_server
from logs import Logger


MODEL='ClientMain'
log = Logger(MODEL).log()



def main(): 
    log.info("=============BEGIN===========")
    log.info('Mega Client server start at %s ' % datetime.datetime.now())
    tcp_server()


    
if __name__=='__main__':
    main()