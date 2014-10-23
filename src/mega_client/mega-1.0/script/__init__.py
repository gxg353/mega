'''
Created on Jul 30, 2014

@author: xchliu

@module:mega_service.mega_client.upgrade
'''

__doc__="""
        scripts used for client func invoking
        all the scripts here can/should use the public mega_client module instead of import the private path 
        
        in fact,scripts will be called in the command line by the worker class,
        and the exit error code and standard output will be logged and used to verdict whether the task runs successfully
"""