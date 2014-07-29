# -*- coding:utf-8 -*-
'''
Created on Jul 29, 2014

@author: xchliu

@module:mega_portal.file_manage
'''
from django import forms


class UploadFileForm(forms.Form):
#    title =forms.CharField(max_length=50)
    file = forms.FileField(
                          # label='Choose a file',
                          # help_text='doc,ppt,pdf etc.'
                           )    
 
    