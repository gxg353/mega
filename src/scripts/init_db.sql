#

use mega;

insert into user(name,stat) values('DBA',1);
insert into business(name,owner)values('None',1);
insert into task (name,type,value,cycle) values('backup',0,'backup_routine',60);
insert into task (name,type,value,cycle) values('slowlog',0,'slowlog_routine',60);
