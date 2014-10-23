# -*- coding:utf-8 -*-
'''
Created on Sep 23, 2014

@author: xchliu

@module:mega_service.report.daily
'''
import sys
sys.path.append("/export/servers/app/mega/src/")
from lib.utils import today
from lib.utils import SendMail
from lib.PyMysql import PyMySQL
from mega_web.console.backup import Backup

MODEL='mega_daily_report'

def backup_report_daily(date=None):
    if not date:
        date=today(1)
    subject='Backup Daily Report for %s' % date
    temail=['wygaoxingang@chinabank.com.cn','wyzhouhuan@chinabank.com.cn','wyliuxiaocheng@chinabank.com.cn']
    sql="select host_ip,port,backup_tool,backup_level,backup_type,timediff(backup_end_time,backup_begin_time) as backup_time,file_size,message,backup_status \
         from backup_history_info where date(backup_begin_time)='%s' order by backup_tool,host_ip;" % date
    _cursor=PyMySQL().query(sql,'dict')
    if _cursor:
        _data=_cursor.fetchall()
    _statics_today=Backup().get_today_statics(date)
    _uninvoked_task=Backup().get_uninvoked_backup(date)

    #generate the email content
    head='<h3>配置总数：%s</h3><h4>备份成功：%s &#9;  备份失败：%s  &#9;   备份未发起：%s</h4>' %(_statics_today.get('total_today',0),_statics_today.get('success_count',0),
                                                                                                    _statics_today.get('failure_count',0),
                                                                 (_statics_today.get('total_today',0)-(_statics_today.get('success_count',0)+_statics_today.get('failure_count',0)))
                                                                                                        )
    body='<table><tr bgcolor="#E6EED5"><td></td><td>IP</td><td>PORT</td><td>工具</td><td>级别</td><td>类型</td><td>时间</td><td>大小(MB)</td><td>结果</td><td>消息</td></tr>'
    footer='<b>More Info:<a href="http://mega.db.cbpmgt.com/console/backup/">mega</a><b>'
    data=''
    alt =True
    counts=1
    for _d in _data:
        if _d.get('backup_status') == 'Y':
            color='bgcolor="#FFFFFF"' if alt else 'bgcolor="#E6EED5"'
        else:
            color='bgcolor="#FF4500"'
        data +='<tr %s><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s </td><td>%s</td><td>%s</td></tr>' %(
                                                                                                            color,counts,
                                                                                                            _d.get('host_ip'),_d.get('port'),
                                                                                                            _d.get('backup_tool'),_d.get('backup_level'),
                                                                                                            _d.get('backup_type'),_d.get('backup_time'),
                                                                                                            _d.get('file_size'),_d.get('backup_status'),
                                                                                                            _d.get('message')
                                                                                                            )
        alt=not alt
        counts+=1
    un_data='<hr>Uninvoked backup:<table>'
    counts=1
    for _t in _uninvoked_task:
        color='bgcolor="#FFE4E1"'
        un_data +='<tr %s><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s </td></tr>' %(
                                                                                                            color,counts,
                                                                                                            _t[1],_t[2],_t[4],_t[5],
                                                                                                            _t[7],_t[14],_t[16]
                                                                                                            )
        counts+=1
    un_data+='</table>'
    body=head+footer+body+str(data)+'</table>'+str(un_data)
    content=str(body)
    result,msg=SendMail(MODEL).sendmail(subject, content, temail)


def main():
    backup_report_daily()

if __name__ == "__main__":
    main()