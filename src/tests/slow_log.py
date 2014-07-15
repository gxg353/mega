'''
Created on Jul 15, 2014

@author: xchliu
'''
import unittest
import sys
sys.path.append("..")

from mega_service.sender import MegaClient

var='''
    {'db_host': '127.0.0.1',
     'port': 3306,
    'start_time':'0000-00-00 00:00:00',
    'user':'xchliu',
    'user_host':'127.0.0.1',
    'query_time': 20,
    'lock_time':12,
    'rows_sent':21,
    'rows_examined':22,
    'sql_text':'select 1',
    'sql_explained':"{test:test}"
}
'''

def test_add_slowlog():
    cmd='add_slow_log'
    c=MegaClient(cmd=cmd)
    print c.run(var)    



if __name__ == "__main__":
    test_add_slowlog()