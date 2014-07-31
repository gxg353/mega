#!/bin/bash

#Created on Jul 31, 2014

#@author: xchliu

#@module:mega_client.mega_client.install

PROJECT="mega_client"
if [[ `id -u` -ne 0 ]];then
	echo 'Need root!'
	exit 1
fi

p_path=`dirname $0`
l_path=`pwd`


cd $p_path && `python  setup.py install`

`ln -sf  $l_path/mega-client.py /etc/init.d/$PROJECT`
