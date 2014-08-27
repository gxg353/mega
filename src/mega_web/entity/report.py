# -*- coding:utf-8 -*-
'''
Created on Aug 18, 2014

@author: xchliu

@module:mega_web.entity.report
'''
from django.db import connection, models
 
class SlowLog(models.Model):
    class Meta(object):
        db_table='report_slowlog'
      
    id = models.AutoField(primary_key=True)
    instance_id=models.IntegerField()
    dbname=models.CharField(max_length=50)
    stattime=models.CharField(max_length=50)
    counts=models.IntegerField()
    

def main():
    return
if __name__ == "__main__":
    main()