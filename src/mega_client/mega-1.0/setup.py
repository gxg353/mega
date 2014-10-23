# -*- coding:utf-8 -*-
'''
Created on Jul 21, 2014

@author: xchliu

@module:mega_service.mega_client.setup
'''

from distutils.core import setup

VERSION='1.0'

setup(name='mega',
      version=VERSION,
      description='Mega client',
      author='XCHLIU',
      author_email='liu.xiaocheng0312@gmail.com',
      py_modules=['mega_client.sender','mega_client.utils','mega_client.logs','mega_client.setting'],
      #url='',
      #packages=['mega_client','mega_client/script'],
      #package_dir={'mypkg': 'src/mypkg'},
      # package_data={'mypkg': ['data/*.dat']},
      #data_files=[('',['install.sh'])]
     )