#!/bin/bash

#used to install application

PROJECT=mega
chmod a+x /export/servers/app/mega/src/mega_service/mega_server.py
ln -sf /export/servers/app/mega/src/mega_service/mega_server.py /etc/init.d/$PROJECT
