# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_service.mega_client.upgrade
'''

from logs import Logger
from sender import MegaClient

MODEL='Upgrade'
log = Logger(MODEL).log()

class Upgrade():
    
    def __init__(self):
        self.cmd='client_upgrade'
        self.c=MegaClient(cmd=self.cmd)
    
    def _run(self):
        self.c.run()