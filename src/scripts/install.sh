#!/bin/bash

#used to install application

PROJECT=mega
APP_DIR='/Users/xchliu/Documents/workspace/mega/src/'

ln -sf $APP_DIR/scripts/$PROJECT_service.sh /etc/init.d/$PROJECT

