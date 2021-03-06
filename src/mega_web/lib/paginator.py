# -*- coding:utf-8 -*-
'''
Created on Jul 1, 2014

@author: xchliu

@module:mega_web.lib.paginator
'''

from django.core.paginator import Paginator

def paginator(object,page_num=1):
    result={}
    if not object:
        return result
    p=Paginator(list(object),15)
    result['pages']=p.num_pages
    result['page_range']=p.page_range
    result['page_data']=p.page(page_num)
    return result