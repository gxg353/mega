# -*- coding:utf-8 -*-
'''
Created on Sep 2, 2014

@author: xchliu

@module:mega_web.resource.vip_manage
'''

from mega_web.entity.models import Vip
from conf.GlobalConf import MSG_ERR_IP



class VipManage():
    '''
    '''
    def __init__(self,request):
        self.vip=request.get('vip')
        self.domain=request.get('domain')
        self.type=request.get('type')
        self.stat=request.get('stat')
        
    def _data_check(self): 
        if not self.vip :
            return False
        return True
    
    def add_vip(self):
        if not self._data_check():
            return False,MSG_ERR_IP
        v=Vip(vip=self.vip,domain=self.domain,type=self.type,stat=self.stat)
        v.save()
        return True,''

class VipGet():
    '''
    '''
    def __init__(self):
        self.vip=Vip
    
    def get_vip_list(self,type=1,count=10):
        if count == 0:
            vip_list=self.vip.objects.filter(type=type).order_by('stat','vip').values()
        else:
            vip_list=self.vip.objects.filter(type=type).order_by('stat','vip')[count].values()
        return vip_list
    
    def get_vip_by_ip(self,vip):
        vip_list=self.vip.objects.filter(vip=vip).values()
        return vip_list

def main():
    return
if __name__ == "__main__":
    main()