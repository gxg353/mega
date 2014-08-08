# -*- coding:utf-8 -*-
'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_client.mega_client.utils
'''
import socket as S
from socket import socket,SOCK_DGRAM,AF_INET
from email import Utils
from email.mime.text import MIMEText
from email import Header
import smtplib

from setting import MAIL_HOST
from logs import Logger

MODEL='Utils'
log = Logger(MODEL).log()


def get_ip_address():
    myname=''
    myip=''
    try:
        myname = S.getfqdn(S.gethostname())
        myip = S.gethostbyname(myname)
    except:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        myip=s.getsockname()[0] 
    return myname,myip

class SendMail():
    '''
        A mail send client in HTML.
        Args:
          subject: subject;
          content: Content in HTML;
          temail: A list() of Recipients;
          femail: sender address, default is 'report.mega@chinabank.com.cn';
          priority: priority
          
       Useage:
          import utils
          s=utils.SendMail('test')
          subject = "Test mail from 172.17.58.25"
          content = "<H1>Test</H1>"
          temail = ("wyliuxiaocheng@chinabank.com.cn",)
          s.sendmail(subject, content, temail)
    '''
    
    DEFAULT_FEMAIL='report.mega@chinabank.com.cn'
    DEFAULT_PRIORITY="3"
    
    def __init__(self,module):
        self.module=module
        
    def sendmail(self,subject,content,temail,femail=DEFAULT_FEMAIL,priority=DEFAULT_PRIORITY):
        log.debug("Get mail task : %s for %s" % (subject,self.module))
        if len(str(subject))*len(content)*len(temail) == 0:
            return False,'illegal argument!'
        mime = MIMEText(content)
        mime['To'] = ", ".join(temail)
        mime['From'] = femail
        mime['Subject'] =  Header.Header(subject,'utf-8')
        mime['X-Priority'] =  priority
        mime['Date'] = Utils.formatdate(localtime = 1)
        try:
            s = smtplib.SMTP(MAIL_HOST)
            s.sendmail(femail, temail, mime.as_string())
            log.info("Mail task:%s %s  :%s" % (self.module,subject,temail))
            return True,''
        except smtplib.SMTPException, se:
            log.error(se)
        finally:
            if s:
                s.close()
 