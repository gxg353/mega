# -*- coding:utf-8 -*-
'''
Created on Aug 1, 2014

@author: xchliu

@module:mega_client.mega_client.script.mega
'''
try:
    from mega_client.sender import MegaClient
except:
    from mega_client.mega_client.sender import MegaClient
    
def sync_file(host='localhost'):
    cmd='sync_file'
    c=MegaClient(host,port=1105,cmd=cmd)
    c.run()


def client_update(host='localhost'):
    cmd='upgrade.py'
    c=MegaClient(host,port=1105,cmd=cmd)
    return c.run(TARGET='python')
    


def main():
    #sync_file()
    client_update()
    return

if __name__ == "__main__":
    main()