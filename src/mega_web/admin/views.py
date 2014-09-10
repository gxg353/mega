# -*- coding:utf-8 -*-
'''
Created on Aug 7, 2014

@author: xchliu

@module:mega_web.admin.views
'''
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,RequestContext

from client_manage import ClientGet
from mega_web.lib import paginator
from mega_service.mega import client_update


def mega_admin(request):
    if request.method=="GET":
        return render_to_response('admin_mega/admin.html')
    else:
        return render_to_response('admin_mega/admin.html')
    
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
    return render_to_response('admin_mega/client.html',{'client_list':client_list,'page_range':page_range,'msg':_msg},context_instance=RequestContext(request))

def login(request):
    next='/login/'
    if request.method == 'GET':
        next = request.GET.get('next','')
        return render_to_response('admin_mega/login.html',{'next':next},RequestContext(request))
    else:
        
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next    = request.POST.get('next','')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if not next:
                next='/'
        return HttpResponseRedirect(next)  

#@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")  
#    return render_to_response('home.html', RequestContext(request))


def main():
    return

if __name__ == "__main__":
    main()