#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,HttpResponse
from django.contrib.auth.decorators import login_required

from resource import instance_manage,server_manage,business_manage,database_manage,resource_manage,user_manage,vip_manage
from console.backup import Backup,Backup_Config
from console.failover import FailoverGet,FailoverManage
from lib import paginator
from lib.meta_data import MetaData 
from mega_portal.file_manage import UploadFileForm
from mega_web.entity.models import Document
from mega_service.task import Task
from mega_web.console.task import TaskManage 
from mega_web.admin.views import * 
from mega_web.tunning import slowlog
from mega_web.monitor import alert_manage

meta_data=MetaData()

@login_required
def home(request):
    slow_log=slowlog.get_chart_total()
    alert_list=alert_manage.get_alert_list()
    return render_to_response('home.html',{'slowlog':slow_log,'alert_list':alert_list},context_instance=RequestContext(request))
   
@login_required
def monitor(request):
    if request.method=='POST':
        alert_id=request.POST.get('alert_id')
        alert_manage.update_alert(alert_id)
    alert_list=alert_manage.get_alert_list()
    return render_to_response('monitor.html',{'alert_list':alert_list},context_instance=RequestContext(request))

@login_required
def console(request):
    if request.method=="GET":
        return render_to_response('console.html',context_instance=RequestContext(request))
    else:
        return render_to_response('console.html',context_instance=RequestContext(request))

def tunning(request):
    if request.method=="GET":
        return render_to_response('tunning.html',context_instance=RequestContext(request))
    else:
        return render_to_response('tunning.html',context_instance=RequestContext(request))

def portal(request):
    if request.method=="GET":
        return render_to_response('portal.html',context_instance=RequestContext(request))
    else:
        return render_to_response('portal.html',context_instance=RequestContext(request))

def fun(request):
    if request.method=="GET":
        return render_to_response('fun.html',context_instance=RequestContext(request))
    else:
        return render_to_response('fun.html',context_instance=RequestContext(request))



#Sub sites
##resource
def instance(request):
    page_num=1
    if request.method=="GET":
        page_num=request.GET.get('page')
        instance_list_all=instance_manage.InstanceGet().get_instance_list(None,0)
    else:
        ip=request.POST.get("ip")
        instance_list_all=instance_manage.InstanceGet().get_instance_list({"ip":ip},0)
    if not page_num:
        page_num=1
    page_data=paginator.paginator(instance_list_all, page_num)
    instance_list=page_data.get('page_data')
    page_range=page_data.get('page_range')
    return render_to_response('instance.html',{'instance_list':instance_list,'page_range':page_range},context_instance=RequestContext(request))

def instance_add(request):
    msg=''
    if request.method=="POST":
        result,msg=instance_manage.InstanceManage(request.POST).add_instance()
        if result:
            msg='Sucess'  
    return render_to_response('instance_add.html',{"business_list":meta_data.business_list(),"owner_list":meta_data.owner_list(),
                                                        "db_type":meta_data.db_type,"level":meta_data.level,
                                                       "ha_type":meta_data.ha_type,"msg":msg,"version_list":meta_data.version,
                                                       "instance_list":meta_data.instance_list()
                                                       },context_instance=RequestContext(request))

def instance_detail(request):
    inst=instance_manage.InstanceGet()
    if request.method=="GET":
        instance_id=request.GET.get('instance_id')
        instance=inst.get_instance(request.GET)
    else:
        instance_id=request.GET.get('instance_id')
        if request.POST.get("type")=="mod":
            instance_manage.InstanceManage(request.POST).mod_instance()    
        else:
            instance_manage.InstanceManage(request.POST).stat_instance()
        instance=inst.get_instance(request.POST)
    instance_base=inst.get_instance_base(instance_id)
    failover=FailoverGet().get_instance_failover(instance_id)
    #database=inst.get_instance_list({"":""}, count, offset)
    return render_to_response('instance_detail.html',{"instance":instance,"readonly":"true","business_list":meta_data.business_list(),
                                                      "owner_list":meta_data.owner_list(),
                                                       "db_type":meta_data.db_type,"level":meta_data.level,
                                                       "ha_type":meta_data.ha_type,"version_list":meta_data.version,
                                                       "instance_list":meta_data.instance_list(),
                                                       "instance_base":instance_base,
                                                       "failover":failover
                                                   },context_instance=RequestContext(request))

##server
def server(request):
    if request.method=="GET":
        page_num=request.GET.get('page')
        server_list_all=server_manage.ServerGet().get_server_list(None, 0)
        if not page_num:
            page_num=1
        page_data=paginator.paginator(server_list_all, page_num)
        server_list=page_data.get('page_data')
        page_range=page_data.get('page_range')
        return render_to_response('server.html',{"server_list":server_list,'page_range':page_range},context_instance=RequestContext(request))
    else:
        ip=request.POST.get('ip')
        if not ip :
            server=server_manage.ServerGet().get_server_list(None, 0)
        else:
            server=[]
            server_id =server_manage.ServerGet().get_server_by_ip(request.POST.get("ip"))
            if server_id:
                server.append(server_manage.ServerGet().get_server_by_id(server_id))
        return render_to_response('server.html',{'server_list':server},context_instance=RequestContext(request))
def server_add(request):
    msg=''
    if request.method=="POST":
        result,msg=server_manage.ServerManage(request.POST).add_server()
        if result:
            msg='Sucess'
    return render_to_response('server_add.html',{'owner_list':meta_data.owner_list(),'os_list':meta_data.os,'msg':msg,
                                                 'plant_list':meta_data.plant_list},
                              context_instance=RequestContext(request))
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
    return render_to_response('server_detail.html',{"server":server,'plant_list':meta_data.plant_list,
                                                    'os_list':meta_data.os,'owner_list':meta_data.owner_list()
                                                    },context_instance=RequestContext(request))
   
#business
def business(request):
    if request.method=="GET":
        page_num=request.GET.get('page')
        business_list_all=business_manage.BusinessGet().get_business_list(None, 100)
        if not page_num:
            page_num=1
        page_data=paginator.paginator(business_list_all,page_num)
        business_list=page_data.get('page_data')
        page_range=page_data.get('page_range')
        return render_to_response('business.html',{"business_list":business_list,'page_range':page_range},context_instance=RequestContext(request))
    else:
        business=request.POST.get('business')
        if not business:
            business_list=business_manage.BusinessGet().get_business_list(None, 10)
        else:
            business_list=business_manage.BusinessGet().get_business_list([business], 10)
        return render_to_response('business.html',{"business_list":business_list},context_instance=RequestContext(request))
def business_add(request):
    if request.method=="GET":
        return render_to_response('business_add.html',{'owner_list':meta_data.owner_list},context_instance=RequestContext(request))
    else:
        result,msg=business_manage.BusinessManage(request.POST).add_business()
        if result:
            msg='Success'
        return render_to_response('business_add.html',{"msg":msg,'owner_list':meta_data.owner_list()},context_instance=RequestContext(request))
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
    return render_to_response('business_detail.html',{"business":business,'owner_list':meta_data.owner_list()},context_instance=RequestContext(request))

#database
def database(request):
    page_range=[]
    if request.method=="GET":
        page_num=request.GET.get('page')
        database_list_all=database_manage.DatabaseGet().get_database_list(None, 0)
        if not page_num:
            page_num=1
        page_data=paginator.paginator(database_list_all, page_num)
        database_list=page_data.get('page_data')
        page_range=page_data.get('page_range')
        return render_to_response('database.html',{"database_list":database_list,'page_range':page_range},context_instance=RequestContext(request))
    else:
        ip=request.POST.get("ip")
        database_list=database_manage.DatabaseGet().get_database_list({"ip":ip})
        if not ip :
            page_range=paginator.paginator(database_list)['page_range']
        return render_to_response('database.html',{"database_list":database_list,'page_range':page_range},context_instance=RequestContext(request))
def database_add(request):
    instance_list=instance_manage.InstanceGet().get_instance_list(None,count=0) #.values("id","ip","port")
    if request.method=="GET":
        return render_to_response('database_add.html',{"instance_list":instance_list,"business_list":meta_data.business_list(),
                                                       "level":meta_data.level,'owner_list':meta_data.owner_list()},context_instance=RequestContext(request))
    else:
        (result,msg)=database_manage.DatabaseManage(request.POST).add_database()
        return render_to_response('database_add.html',{"msg":msg,"instance_list":instance_list,"business_list":meta_data.business_list,
                                                       "level":meta_data.level,'owner_list':meta_data.owner_list},context_instance=RequestContext(request))
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
    return render_to_response('database_detail.html',{"database":database,
                                                      "instance_list":meta_data.instance_list(),"business_list":meta_data.business_list(),
                                                      "level":meta_data.level,'owner_list':meta_data.owner_list()},context_instance=RequestContext(request))

#user
def user(request):
    if request.method=="GET":
        user_list=user_manage.UserGet().get_user_list('')
        return render_to_response('user.html',{"user_list":user_list},context_instance=RequestContext(request))
    else:
        user=request.POST.get("user")
        user_list=user_manage.UserGet().get_user_list({"name":user})
        return render_to_response('user.html',{"user_list":user_list},context_instance=RequestContext(request))

def user_add(request):
    if request.method=="GET":
        user_list=user_manage.UserGet().get_user_list('')
        return render_to_response('user_add.html',{"user_list":user_list},context_instance=RequestContext(request))
    else:
        result,msg=user_manage.UserManage(request.POST).user_add()
        return render_to_response('user_add.html',{"msg":msg},context_instance=RequestContext(request))


def user_detail(request):
    msg=''
    if request.method=="POST":
        user_id=request.POST.get('user_id')
        if request.POST.get("type")=='mod':
            result,msg=user_manage.UserManage(request.POST).user_mod()
        else:
            result,msg=user_manage.UserManage(request.POST).user_stat()  
    else:
        user_id=request.GET.get('user_id')
    user=user_manage.UserGet().get_user_by_id(user_id)
    return render_to_response('user_detail.html',{"user":user,"msg":msg,},context_instance=RequestContext(request))

#vip
def vip(request):
    msg=''
    if request.method=="GET":
        vip=request.GET.get('vip')
        if vip:
            vip_list=vip_manage.VipGet().get_vip_by_ip(vip)
        else:
            vip_list=meta_data.vip_list()
    else:
        if request.POST.get('action') == 'add':                        
            result,msg=vip_manage.VipManage(request.POST).add_vip()
        else:
            result,msg=vip_manage.VipManage(request.POST).mod_vip()
        vip_list=meta_data.vip_list()        
    return render_to_response('vip.html',{"msg":msg,'vip_list':vip_list,'plant_list':meta_data.plant_list},context_instance=RequestContext(request))

#backup

def backup(request):
    if request.method=="GET":
        page=request.GET.get('page')
        backup_list_all=Backup().get_newest_backup_list()
    else:
        page=request.POST.get('page')
        ip=request.POST.get('ip')
        backup_list_all=Backup().get_newest_backup_list(ip=ip)
    if not page:
        page=1
    page_data=paginator.paginator(backup_list_all, page)
    page_range=page_data.get('page_range')
    backup_list=page_data.get('page_data')
    today_static=Backup().get_today_statics()
    return render_to_response('backup.html',{"backup_list_all":backup_list,"page_range":page_range,"today_static":today_static},context_instance=RequestContext(request))

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
def backup_config_list(request):
    if request.method=="GET":
        page=request.GET.get('page')
        backup_list_all=Backup().get_config_list()
    else:
        page=request.POST.get('page')
        ip=request.POST.get('ip')
        backup_list_all=Backup().get_config_list(ip=ip)
    if not page:
        page=1
    page_data=paginator.paginator(backup_list_all, page)
    page_range=page_data.get('page_range')
    backup_list=page_data.get('page_data')
    return render_to_response('backup_config_list.html',{"backup_list_all":backup_list,"page_range":page_range},context_instance=RequestContext(request))

def document(request):
    if request.method=="GET":
        form=UploadFileForm()
    else:
        form=UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            _new_doc=Document(file=request.FILES['file'])
            _new_doc.save()
    documents=Document.objects.all()
    
    return render_to_response('document.html',{'form':form ,'documents':documents},context_instance=RequestContext(request))

def task(request):
    if request.method=="GET":
        page=request.GET.get('page')
        task_list=Task().get_task_list(-1)
    if not page:
        page=1
    page_data=paginator.paginator(task_list, page)
    page_range=page_data.get('page_range')
    task_list=page_data.get('page_data')
    return render_to_response('task.html',{"task_list":task_list,"page_range":page_range},context_instance=RequestContext(request))

def task_add(request):
    msg=''
    if request.method == "POST" :
        result,msg=TaskManage(request.POST).task_add()
    return render_to_response('task_add.html',{'owner_list':meta_data.owner_list(),'msg':msg},context_instance=RequestContext(request))

def task_detail(request):
    msg=''
    if request.method=='GET':
        task=TaskManage(request.GET).get_task_by_id()
    else:
        _task=TaskManage(request.POST)
        result,msg=_task.task_mod()
        task=_task.get_task_by_id()
    return render_to_response('task_detail.html',{'task':task,'owner_list':meta_data.owner_list(),'msg':msg},context_instance=RequestContext(request))

#slow log
def slowlog_config(request):
    if request.method=='GET':
        result=instance_manage.InstanceManage(request.GET).stat_instance_slowlog()
    return render_to_response('slowlog_config.html',{'instance_list':meta_data.instance_list()},context_instance=RequestContext(request))

def slowlog_report(request):
    if request.method=='GET':
        begin=end=None
    else:
        begin=request.POST.get('begin_date')
        end=request.POST.get('end_date')
    groupbyinstance=slowlog.get_chart_groupbyinstance(begin,end)
    total=slowlog.get_chart_total(None,begin,end)
    groupbytime=slowlog.get_chart_groupbytime(begin,end)
    topsql=slowlog.get_chart_topsql(begin,end)
    return render_to_response('slowlog_report.html',{'groupbyinstance':groupbyinstance,'total':total,'topsql':topsql,'groupbytime':groupbytime},
                              context_instance=RequestContext(request))

def slowlog_sql(request):
    msg=''
    if request.method=='GET':
        hash_code=request.GET.get('hash_code')
    else:
        hash_code=request.POST.get('hash_code')
        msg=slowlog.add_opt_record(request.POST)
    groupbyinstance=slowlog.get_sql_hosts(hash_code)
    total=slowlog.get_sql_time(hash_code)
    sql_info=slowlog.get_sql_info(hash_code)
    opt_record=slowlog.get_opt_record(hash_code)
    return render_to_response('slowlog_report_sql.html',{'groupbyinstance':groupbyinstance,'total':total,'sql_info':sql_info,'msg':msg,"opt_record":opt_record},
                              context_instance=RequestContext(request))

def slowlog_instance(request):
    if request.method=='GET':
        begin=end=None
        instance_id=request.GET.get('instance_id',1)
    else:
        begin=request.POST.get('begin_date')
        end=request.POST.get('end_date')
        instance_id=request.POST.get('instance_id',1)
    
    #total=slowlog.get_chart_total(instance_id,begin,end)
    total=slowlog.get_chart_total(instance_id)
    instance=instance_manage.InstanceGet().get_instance_by_id(instance_id)
    groupbydb=slowlog.get_chart_groupbydb(instance_id,begin,end)
    topsql=slowlog.get_instance_topsql(instance_id,begin,end)
    return render_to_response('slowlog_report_instance.html',{'instance_list':meta_data.instance_list(),'total':total,'instance':instance,'groupbydb':groupbydb,'topsql':topsql},
                              context_instance=RequestContext(request))
@login_required    
def failover(request):
    msg=''
    if request.method=='GET':
        ip=request.GET.get('ip')
        failover_list=FailoverGet().get_failover_list(ip=ip)

    if request.method=='POST':
        action=request.POST.get('action')
        if action=='add':
            result,msg=FailoverManage(request.POST).add_failover()
        else:
            result,msg=FailoverManage(request.POST).mod_failover()
        failover_list=FailoverGet().get_failover_list()
    wvips=meta_data.vip_list(type=1)
    rvips=meta_data.vip_list(type=2)
    managers=meta_data.server_list(('type',2))
    masters=meta_data.instance_list({'i.role':1})
    return render_to_response('failover.html',{'msg':msg,'wvips':wvips,'rvips':rvips,'managers':managers,'masters':masters,'failover_list':failover_list},context_instance=RequestContext(request))

def switch(request):    
    failover=request.GET
    slaves=[]
    if failover.get('method'):
        result=FailoverManage(failover).change_master(failover.get('id'),failover.get('slave'),failover.get('method'))
        #return HttpResponse('123')
        return HttpResponse(result)
    else:
        masterid=failover.get('masterid')
        slaves=instance_manage.InstanceGet().get_instance_slaves(masterid)
    return render_to_response('switch.html',{'failover':failover,'slaves':slaves,'methods':meta_data.failover_method})

@login_required    
def switch_detail(request):
    '''
        only recieve get request
    '''
    if request.method=='POST':
        return render_to_response('switch_detail.html')
    #failover
    failoverid=request.GET.get('failoverid')
    new_masterid=request.GET.get('new_master')
    method=request.GET.get('method','')    
    new_master=instance_manage.InstanceGet().get_instance_by_id(new_masterid)
    failover=FailoverGet().get_failover_by_id(failoverid)
    if failover:
        failover['method']=method
        failover['new_master']=new_master.get('ip')+':'+str(new_master.get('port'))
        #history
        failover_his=FailoverGet().get_failover_history(failoverid)
        #log
        record_id=FailoverGet().get_newest_record(failoverid)
        failover_log=FailoverGet().get_failover_history_detail(record_id)
        result=FailoverGet().get_failover_result(record_id)
        failover['result']=result.get('result')
        return render_to_response('switch_detail.html',{'failover':failover,'failover_his':failover_his,'failover_log':failover_log})
    return render_to_response('switch_detail.html')

@login_required    
def baseinfo(request):
    return render_to_response('baseinfo.html')

@login_required    
def baseinfo_instance(reqeust):
    return render_to_response('baseinfo_instance.html')

@login_required    
def status(request):    
    return render_to_response('status.html')

@login_required    
def report(request):    
    return render_to_response('report.html')

def my_404_view(request):
    response = render_to_response('404.html',context_instance=RequestContext(request))
    response.status_code = 404
    return response
    
def my_500_view(request):
    return render_to_response('500.html')

