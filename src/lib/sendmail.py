'''
Created on Jul 9, 2014

@author: xchliu
'''
import smtplib  
from email.mime.text import MIMEText  

#####################  
mail_host="smtp.163.com"
mail_user=""  
mail_pass=""  
mail_postfix="163.com"  
######################  

class SendMail(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
def send_mail(to_list,sub,content):  
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content)  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP(mail_host)  
        s.starttls()
        s.login(mail_user,mail_pass)  
        s.sendmail(me, to_list, msg.as_string())  
        s.close()  
        return True  
    except Exception, e:  
#        print str(e)  
        return False  
if __name__ == '__main__':  
    if send_mail(mailto_list,"test","test"):  
        print "1"  
    else:  
        print "2"           