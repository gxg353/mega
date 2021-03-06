# -*- coding:utf-8 -*-
'''
Created on Jul 2, 2014

@author: xchliu

@module:release.db_schema_his
'''

#2014-07-03
alter table business add unique index idx_name(name);
alter table `databases` add unique index idx_name(name);
alter table instance add unique index idx_instance(ip,port);
alter table server add unique index idx_ip(ip);


#2014-07-03
alter table instance add column version varchar(10) not null default '0';
alter table task add column script varchar(50) not null default '';
 CREATE TABLE `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

#2014-08-04
alter table task add column stat int not null default 1;
alter table task change target target varchar(200) not null default '';
alter table task_log add column stat int not null default 0;
alter table task_log change run_counts run_counts int not null default 0;

#2014-0-15
alter table  instance add column slowlog int not null default 1;

#2014-08-20
alter table slowlog_info add hash_code varchar(50) not null after id;
alter table slowlog_info add instance_id int not null after hash_code;
alter table slowlog_info add stat int not null default 0;

#2014-08-27
CREATE TABLE `slowlog_opt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash_code` varchar(64) NOT NULL,
  `opt_method` varchar(50) NOT NULL,
  `opt_explain` varchar(200) NOT NULL,
  `opt_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

#2014-09-25
alter table server add column plant varchar(50) not null default '';

2014-10-17
alter table instance add cnf_file varchar(100) not null default '';
