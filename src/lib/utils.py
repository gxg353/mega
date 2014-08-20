import re
import datetime

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
    if not format:
        format='%Y-%m-%d'
    if day:
        return (datetime.datetime.now()-datetime.timedelta(days=day)).strftime(format)
    else:
        return datetime.datetime.today().strftime(format)