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
    os=GlobalConf.OS
    business_list=business_manage.BusinessGet().get_business_list(None).values("id","name")
    owner_list=user_manage.UserGet().get_user_list(None,0)
    instance_list=instance_manage.InstanceGet().get_instance_list(None) #.values("id","ip","port")
