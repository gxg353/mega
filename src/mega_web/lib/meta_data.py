'''
Created on Jul 1, 2014

@author: xchliu
'''
from conf import GlobalConf
from mega_web.resource import business_manage,user_manage,instance_manage

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
    

    def business_list(self):
        return business_manage.BusinessGet().get_business_list(None,count=1000).values()
    
    def owner_list(self):
        return user_manage.UserGet().get_user_list(None,count=0)
    
    def instance_list(self):
        return instance_manage.InstanceGet().get_instance_list(None,count=0) #.values("id","ip","port")