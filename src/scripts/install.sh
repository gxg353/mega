#!/bin/bash

#used to install application

PROJECT=mega
chmod a+x /export/servers/app/mega/src/mega_service/mega_main.py
ls -sf /export/servers/app/mega/src/mega_service/mega_main.py /etc/init.d/$PROJECT
