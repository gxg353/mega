# -*- coding:utf-8 -*-
'''
Created on Jun 26, 2014

@author: xchliu

@module:mega_web.resource.user_manage
'''
from mega_web.entity.models import Users
from conf.GlobalConf import DEFAULT_PWD,MSG_ERR_NAME,STAT_ONLINE

class UserManage():
    def __init__(self,user_info):
        self.user=Users
        self.user_id=user_info.get("user_id")
        self.user_name=user_info.get("name")
        self.user_sign=user_info.get("sign")
        self.user_role=user_info.get("role")
        self.user_pid=user_info.get("pid")
        self.user_pwd=user_info.get("pwd")
        self.user_phone=user_info.get("phone")
        self.msg=''
    def user_add(self):
        if not self.data_check():
            return False,self.msg
        _user=Users(name=self.user_name,role=self.user_role,sign=self.user_sign,p_id=self.user_pid,pwd=self.user_pwd,phone=self.user_phone,stat=STAT_ONLINE)
        _user.save()
        self.msg='success'
        return True,self.msg
    def user_mod(self):
        if not self.data_check():
            return False,self.msg
        _user=self.user.objects.get(id=self.user_id)
        _user.name=self.user_name
        _user.role=self.user_role
        _user.sign=self.user_sign
        _user.p_id=self.user_pid
        _user.pwd=self.user_pwd
        _user.phone=self.user_phone
        _user.save()
        self.msg='success'
        return True,self.msg
    def user_stat(self):
        if not self.user_id:
            return False,self.msg
        _user=self.user.objects.get(id=self.user_id)
        if _user.stat == 1:
            _user.stat=0
        else:
            _user.stat=1
        _user.save()
        return True,self.msg
    def data_check(self):
        if not self.user_name:
            self.msg=MSG_ERR_NAME
            return False
        if not self.user_role:
            self.user_role=1
        if not self.user_sign:
            self.user_sign=''
        if not self.user_pid:
            self.user_pid=1
        if not self.user_pwd:
            self.user_pwd=DEFAULT_PWD
        if not self.user_phone:
            self.user_phone=0
        return True
class UserGet():
    def __init__(self):
        self.user=Users
    def get_user_list(self,str_filter,count=10,offset=0):
        result=None
        
        if not str_filter:
            str_filter=''
        if len(str_filter) ==0:
            if count==0:
                result=self.user.objects.all().order_by('-stat').values()
            else:
                result=self.user.objects.all().order_by('-stat')[offset:count].values()
        else:
            value=str_filter['name']            
            if len(value) <> 0:
                result=self.user.objects.filter(name=value)[offset:count].values()
            else:
                result=self.user.objects.all().order_by('-stat').values()

        return result
    def get_user_by_id(self,user_id):
        if not user_id:
            return False
        result=self.user.objects.filter(id=user_id).values()
        if len(result)>0:
            return result[0]
        return False