# -*- coding:utf-8 -*-
'''
Created on Jul 4, 2014

@author: xchliu

@module:mega_web.charts.visit
'''
from django.utils.simplejson
from mega_web.entity.models import  Server
from chartit import DataPool, Chart

def Visit(request):
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Server.objects.all()},
              'terms': [
                'id',
                'ip',
                'name']}
             ])
    
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'id': [
                    'name',
                    'ip']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})
    return cht