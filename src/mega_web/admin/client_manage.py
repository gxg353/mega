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
        self.LIFECYCLE=300
        
    def get_client_list(self):
        client_list=self.client.objects.all().values().order_by("-heartbeat")
        for client in client_list:
            _server=self.server.objects.filter(id=client['server_id'])
            if _server:
                client['ip']=_server.values('ip')[0]['ip']
            _heartbeat=(datetime.datetime.now()-client['heartbeat']).seconds
            if _heartbeat > self.LIFECYCLE:
                client['stat']=0
            else:
                client['stat']=1
        return client_list
    def get_client_statics(self):
        count={}
        _time=datetime.datetime.now()-datetime.timedelta(seconds=self.LIFECYCLE)
        count['server']=Server.objects.filter(stat__gt=0).count()
        count['online']=Client.objects.filter(heartbeat__gt=_time).count()
        count['offline']=Client.objects.filter(heartbeat__lt=_time).count()
        return count

def main():
    return
if __name__ == "__main__":
    main()