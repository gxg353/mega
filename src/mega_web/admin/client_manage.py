# -*- coding:utf-8 -*-
'''
Created on Aug 7, 2014

@author: xchliu

@module:mega_web.admin.client_manage
'''
import datetime
from mega_web.entity.models import Client,Server

class ClientGet():
    '''
    '''
    def __init__(self):
        self.client=Client
        self.server=Server
        
    def get_client_list(self):
        client_list=self.client.objects.all().values().order_by("-heartbeat")
        for client in client_list:
            client['ip']=self.server.objects.filter(id=client['server_id']).values('ip')[0]['ip']
            _heartbeat=(datetime.datetime.now()-client['heartbeat']).seconds
            if _heartbeat > 300:
                client['stat']=0
            else:
                client['stat']=1
        return client_list
    
def main():
    return
if __name__ == "__main__":
    main()