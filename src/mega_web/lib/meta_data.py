'''
Created on Jul 1, 2014

@author: xchliu
'''
from conf import GlobalConf
from mega_web.resource import business_manage,user_manage,instance_manage,vip_manage,server_manage

class MetaData(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    db_type=GlobalConf.DB_TYPE
    ha_type=GlobalConf.HA_TYPE
    level=GlobalConf.LEVEL
    version=GlobalConf.VERSION
    os=GlobalConf.OS
    failover_method=GlobalConf.FAILOVER
    plant_list=GlobalConf.PLANT

    def business_list(self):
        return business_manage.BusinessGet().get_business_list(None,count=1000).values()
    
    def owner_list(self):
        return user_manage.UserGet().get_user_list(None,count=0)
    
    def instance_list(self,filter=None):
        return instance_manage.InstanceGet().get_instance_list(filter,count=0) #.values("id","ip","port")

    def vip_list(self,type=None):
        wvips=vip_manage.VipGet().get_vip_list(count=0)
        rvips=vip_manage.VipGet().get_vip_list(type=2,count=0)
        if type==1:
            return wvips
        elif type == 2:
            return rvips
        else:
            return list(wvips)+list(rvips)
    
    def server_list(self,filter=None):
        return server_manage.ServerGet().get_server_list(filter,count=0)
        
        