#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response,RequestContext

from resource import instance_manage,server_manage,business_manage,database_manage,resource_manage
from console.backup import Backup,Backup_Config
def home(request):
    if request.method=="GET":
        return render_to_response('home.html')
    else:
        return render_to_response('home.html')
def monitor(request):
    if request.method=="GET":
        return render_to_response('monitor.html')
    else:
        return render_to_response('monitor.html')
def console(request):
    if request.method=="GET":
        return render_to_response('console.html')
    else:
        return render_to_response('console.html')
def portal(request):
    if request.method=="GET":
        return render_to_response('portal.html')
    else:
        return render_to_response('portal.html')


def fun(request):
    if request.method=="GET":
        return render_to_response('fun.html')
    else:
        return render_to_response('fun.html')
    
def resource(request):
    if request.method=="GET":
        count=resource_manage.get_total_count()
        return render_to_response('resource.html',{'count':count})
    else:
        return render_to_response('resource.html')

#Sub sites
##resource
def instance(request):
    if request.method=="GET":
        instance_list=instance_manage.InstanceGet().get_instance_list(None,10)
        return render_to_response('instance.html',{'instance_list':instance_list})
    else:
        return render_to_response('instance.html')
def instance_add(request):
    if request.method=="GET":
        business_list=business_manage.BusinessGet().get_business_list(None).values("id","name")
        return render_to_response('instance_add.html',{"business_list":business_list},context_instance=RequestContext(request))
    else:
        result,msg=instance_manage.InstanceManage(request.POST).add_instance()
        if result:
            msg='Sucess'  
        business_list=business_manage.BusinessGet().get_business_list(None).values("id","name")  
        return render_to_response('instance_add.html',{"msg":msg,"business_list":business_list},context_instance=RequestContext(request))
def instance_detail(request):
    if request.method=="GET":
        instance=instance_manage.InstanceGet().get_instance(request.GET)
    else:
        if request.POST.get("type")=="mod":
            instance_manage.InstanceManage(request.POST).mod_instance()    
            instance=instance_manage.InstanceGet().get_instance(request.POST)
        else:
            instance_manage.InstanceManage(request.POST).stat_instance()
            instance=instance_manage.InstanceGet().get_instance_by_id()
    if instance.get("stat")==1:
        stat_action='下'
    else:
        stat_action='上'
    return render_to_response('instance_detail.html',{"instance":instance,"readonly":"true","stat_action":stat_action},context_instance=RequestContext(request))

##server
def server(request):
    if request.method=="GET":
        server_list=server_manage.ServerGet().get_server_list(None, 10)
        return render_to_response('server.html',{"server_list":server_list},context_instance=RequestContext(request))
    else:
        return render_to_response('server.html')
def server_add(request):
    if request.method=="GET":
        return render_to_response('server_add.html',context_instance=RequestContext(request))
    else:
        server_manage.ServerManage(request.POST).add_server()
        return render_to_response('server_add.html',context_instance=RequestContext(request))
def server_detail(request):
    if request.method=="GET":
        server=server_manage.ServerGet().get_server(request.GET)
    else:
        if request.POST.get("type")=="mod":
            server_manage.ServerManage(request.POST).mod_server()
            server=server_manage.ServerGet().get_server(request.POST)
        else:
            server_manage.ServerManage(request.POST).stat_server()
            server=server_manage.ServerGet().get_server(request.POST)
    if server.get("stat")==1:
        stat_action='下'
    else:
        stat_action='上'
    return render_to_response('server_detail.html',{"server":server,"stat_action":stat_action},context_instance=RequestContext(request))
   
#business
def business(request):
    if request.method=="GET":
        business_list=business_manage.BusinessGet().get_business_list(None, 10)
        return render_to_response('business.html',{"business_list":business_list},context_instance=RequestContext(request))
    else:
        return render_to_response('server.html')
def business_add(request):
    if request.method=="GET":
        return render_to_response('business_add.html',context_instance=RequestContext(request))
    else:
        result,msg=business_manage.BusinessManage(request.POST).add_business()
        return render_to_response('business_add.html',{"msg":msg},context_instance=RequestContext(request))
def business_detail(request):
    if request.method=="GET":
        business=business_manage.BusinessGet().get_business(request.GET)
    else:
        if request.POST.get("type")=="mod":
            business_manage.BusinessManage(request.POST).mod_business()
            business=business_manage.BusinessGet().get_business(request.POST)
        else:
            business_manage.BusinessManage(request.POST).stat_business()
            business=business_manage.BusinessGet().get_business(request.POST)
    if business.get("stat")==1:
        stat_action='下'
    else:
        stat_action='上'
    return render_to_response('business_detail.html',{"business":business,"stat_action":stat_action},context_instance=RequestContext(request))

#database
def database(request):
    if request.method=="GET":
        database_list=database_manage.DatabaseGet().get_database_list(None, 10)
        return render_to_response('database.html',{"database_list":database_list},context_instance=RequestContext(request))
    else:
        return render_to_response('database.html')
def database_add(request):
    instance_list=instance_manage.InstanceGet().get_instance_list(None) #.values("id","ip","port")
    business_list=business_manage.BusinessGet().get_business_list(None).values("id","name")
    if request.method=="GET":
        return render_to_response('database_add.html',{"instance_list":instance_list,"business_list":business_list},context_instance=RequestContext(request))
    else:
        (result,msg)=database_manage.DatabaseManage(request.POST).add_database()
        return render_to_response('database_add.html',{"msg":msg,"instance_list":instance_list,"business_list":business_list},context_instance=RequestContext(request))
def database_detail(request):
    if request.method=="GET":       
        database=database_manage.DatabaseGet().get_database(request.GET)
    else:
        if request.POST.get("type")=="mod":
            database_manage.DatabaseManage(request.POST).mod_database()
            database=database_manage.DatabaseGet().get_database(request.POST)
        else:
            database_manage.DatabaseManage(request.POST).stat_database()
            database=database_manage.DatabaseGet().get_database(request.POST)
    if database.get("stat")==1:
        stat_action='下'
    else:
        stat_action='上'
    return render_to_response('database_detail.html',{"database":database,"stat_action":stat_action},context_instance=RequestContext(request))

#backup

def backup(request):
    if request.method=="GET":
        backup_list=Backup().get_newest_backup_list()
        for i in  backup_list:
            print i
        return render_to_response('backup.html',{"backup_list_all":backup_list},context_instance=RequestContext(request))
    else:
        return render_to_response('backup.html')

def backup_config(request):
    backup_type=Backup_Config().backup_type
    backup_tool=Backup_Config().backup_tool
    backup_level=Backup_Config().backup_level
    backup_cycle=Backup_Config().backup_cycle
    backup={"stat":'ON'}
    if request.method=="GET":
        ip=request.GET.get("ip")
        port=request.GET.get("port")
        instance={"ip":ip,"port":port}
        config_list,msg=Backup().get_config_by_instance(ip,port)
        backup["msg"]=msg
        return render_to_response('backup_config.html',{"config_list":config_list,"instance":instance,"backup_tool":backup_tool,
                                                        "backup_type":backup_type,"backup_level":backup_level,"backup_cycle":backup_cycle,
                                                        "backup":backup},context_instance=RequestContext(request))
    else:
        ip=request.POST.get("ip")
        port=request.POST.get("port")
        instance={"ip":ip,"port":port}
        config_list,msg=Backup().get_config_by_instance(ip,port)
        backup["msg"]=msg
        result=Backup_Config().config_deliver(request.POST)
        return render_to_response('backup_config.html',{"instance":instance,"config_list":config_list,"backup_tool":backup_tool,
                                                        "backup_type":backup_type,"backup_level":backup_level,"backup_cycle":backup_cycle},context_instance=RequestContext(request))

def my_404_view(request):
        return render_to_response('404.html')
def my_500_view(request):
        return render_to_response('500.html')

#t = get_template('current_datetime.html')
#    html = t.render(Context({'current_date': now}))
#    return HttpResponse(html)