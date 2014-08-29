from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from views import home,monitor,console,resource,portal,fun,tunning
from views import instance,instance_add,instance_detail
from views import server,server_add,server_detail
from views import business,business_add,business_detail
from views import database,database_add,database_detail
from views import backup,backup_config,backup_config_list
from views import task,task_add,task_detail
from views import user,user_add,user_detail
from views import slowlog_config,slowlog_report,slowlog_sql,slowlog_instance
from views import document
from views import vip
from views import document

from views import my_404_view,my_500_view
from views import admin,client


from django.conf import settings
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

#for error catch
handler404 = my_404_view
handler500 = my_500_view


urlpatterns = patterns('',
    url(r'^$',home),
    url(r'^resource/$',resource),
    url(r'^portal/$',portal),
    url(r'^monitor/$',monitor),
    url(r'^tunning/$',tunning),
    url(r'console/$',console),
    url(r'admin/$',admin),

    
#django
#    (r'^admin/', include(admin.site.urls)),

#sub url
    url(r'^resource/instance/$',instance),
    url(r'^resource/instance_add/$',instance_add),
    url(r'^resource/instance_detail/$',instance_detail),
    
    url(r'^resource/server/$',server),
    url(r'^resource/server_add/$',server_add),
    url(r'^resource/server_detail/$',server_detail),

    url(r'^resource/business/$',business),
    url(r'^resource/business_add/$',business_add),
    url(r'^resource/business_detail/$',business_detail),

    url(r'^resource/database/$',database),
    url(r'^resource/database_add/$',database_add),
    url(r'^resource/database_detail/$',database_detail),
    
    url(r'^resource/user/$',user),
    url(r'^resource/user_add/$',user_add),
    url(r'^resource/user_detail/$',user_detail),
    
    url(r'^resource/vip/$',vip),
    
    
    url(r'^console/backup/$',backup),
    url(r'^console/backup/backup_config/$',backup_config),
    url(r'^console/backup/backup_config_list/$',backup_config_list),

    url(r'^console/task/$',task),
    url(r'^console/task/task_add/$',task_add),
    url(r'^console/task/task_detail/$',task_detail),


    url(r'^tunning/slowlog/config/$',slowlog_config),
    url(r'^tunning/slowlog/report/$',slowlog_report),
    url(r'^tunning/slowlog/report/sql/$',slowlog_sql),
    url(r'^tunning/slowlog/report/instance/$',slowlog_instance),

    url(r'^portal/document/$',document),
    
    url(r'^admin/client/$',client),
    
#for static like css ,js ,ima,music     
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_URLS },name="static"),

#other
    url(r'^fun/$',fun),
    

)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)