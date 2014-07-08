# -*- coding:utf-8 -*-
'''
Created on Jul 4, 2014

@author: xchliu

@module:mega_web.charts.visit
'''
from django.utils import simplejson
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
                'ip'
                ]}
             ])
    
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': True},
                'terms':{
                  'ip': [
                    'id'
                    ]
                }},
               {'options':{
                  'type': 'column',
                  'stacking': True},
                'terms':{
                  'ip': [
                    'id'
                    ]
                }}
               ],
            chart_options =
              {'title': {
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})
    return cht