# -*- coding:utf-8 -*-
'''
Created on Jul 2, 2014

@author: xchliu

@module:release.db_schema_his
'''

#2014-07-03
#alter table business add unique index idx_name(name);
#alter table `databases` add unique index idx_name(name);
#alter table instance add unique index idx_instance(ip,port);
#alter table server add unique index idx_ip(ip);


#2014-07-03
alter table instance add column version varchar(10) not null default '0';
alter table task add column script varchar(50) not null default '';
 CREATE TABLE `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;