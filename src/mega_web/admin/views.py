# -*- coding:utf-8 -*-
'''
Created on Aug 7, 2014

@author: xchliu

@module:mega_web.admin.views
'''
from django.shortcuts import render_to_response,RequestContext
from client_manage import ClientGet
from mega_web.lib import paginator
from mega_service.mega import client_update

def admin(request):
    if request.method=="GET":
        return render_to_response('admin/admin.html')
    else:
        return render_to_response('admin/admin.html')
    
def client(request):
    _msg=''
    client_list=ClientGet().get_client_list()
    if request.method=="GET":
        page=request.GET.get('page')
        action = request.GET.get('action')
        host=request.GET.get('ip')
        print action,host
        if action == 'client_upgrade' and host:
            result=client_update(host)
            if result:
                _msg='success'
            else:
                _msg='failure'
    else:
        page=request.POST.get('page')
    if not page:
        page=1
    page_data=paginator.paginator(client_list, page)
    page_range=page_data.get('page_range')
    client_list=page_data.get('page_data')
    return render_to_response('admin/client.html',{'client_list':client_list,'page_range':page_range,'msg':_msg},context_instance=RequestContext(request))

def main():
    return

if __name__ == "__main__":
    main()