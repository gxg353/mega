import re
import time
import datetime
from email import Utils
from email.mime.text import MIMEText
from email import Header
import smtplib
import httplib

from conf.settings import EMAIL_SERVER,SMS_SERVER

def check_ip(ip):
    '''
    check the ip address is correct or not
    '''
    result=False
    if ip:
        ip_match = re.match('((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?$)',ip) 
    if ip_match:
        result=True
    return result
def is_int(value):
    try:
        if not isinstance(int(value),int):
            return False
    except:
        return False
def today(day=None,format=None):
    '''
        if day is given ,return the date N(day) days ago 
        else is today
    '''
    if not format:
        format='%Y-%m-%d'
    if day:
        return (datetime.datetime.now()-datetime.timedelta(days=day)).strftime(format)
    else:
        return datetime.datetime.today().strftime(format)

def now(format=None):
    '''
        return current time 
    '''
    if not format:
        format='%Y-%m-%d %X'
    return time.strftime(format, time.localtime())
    
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
#        log.debug("Get mail task : %s for %s" % (subject,self.module))
        if len(str(subject))*len(content)*len(temail) == 0:
            return False,'illegal argument!'
        mime = MIMEText(content,'html', 'utf-8')
        mime['To'] = ", ".join(temail)
        mime['From'] = femail
        mime['Subject'] =  Header.Header(subject,'utf-8')
        mime['X-Priority'] =  priority
        mime['Date'] = Utils.formatdate(localtime = 1)
        try:
            s = smtplib.SMTP(EMAIL_SERVER)
            s.sendmail(femail, temail, mime.as_string())
#            log.info("Mail task:%s %s  :%s" % (self.module,subject,temail))
            return True,''
        except smtplib.SMTPException, se:
            return False,se
#            log.error(se)
    
def sms(to_mail,msg):
    '''
        to_mail: 1111,222,333
        msg: 'test'
    '''
    if not to_mail or not msg:
        return False
    url="http://%s:%s/sms.php?phone=%s&sms=%s" % (SMS_SERVER[0],SMS_SERVER[1],to_mail,msg)
    try:
        conn=httplib.HTTPConnection(SMS_SERVER[0],port=SMS_SERVER[1])
        conn.request('GET', url)
        response=conn.getresponse()
        if response.getheaders():
            return True
    except Exception as ex:
#        log.error(ex)
        return False