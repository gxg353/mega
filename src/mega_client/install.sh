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

mkdir -p /var/log/mega/ 
chmod -R 777 /var/log/mega/

cd $p_path
echo "install python package..."
python  setup.py install
chmod a+x $l_path/mega_client/mega_client.py
ln -sf  $l_path/mega_client/mega_client.py /etc/init.d/$PROJECT
echo "add to rc.local"
echo "python /etc/init.d/$PROJECT restart" >>/etc/rc.local
echo "start service..." 
python /etc/init.d/$PROJECT restart
echo "done"
