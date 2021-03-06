# Slow Log 慢查询分析统计
##功能点
 * 收集查询明细及执行计划
 * 按维度聚合分析慢查询
 * 趋势分析
 
##配置要求
* 开启慢查询
* 设置慢查询登记时间
* 

##流程
 收集脚本 -> sender -> listener -> worker ->api:slowlog -> db : slow_log 
 
 离线分析模块 -> 统计数据模块 ->  web 页面
 
 
 
##接口定义

	var='''
    	{'db_host': '127.0.0.1',
	     'port': 3306,
    	'start_time':'0000-00-00 00:00:00',
	    'user':'xchliu',
	    'user_host':'127.0.0.1',
    	'query_time': 20,
	    'lock_time':12,
	    'rows_sent':21,
	    'rows_examined':22,
	    'sql_text':'select 1',
	    'sql_explained':"{test:test}"
	}
	'''


##统计项
1. 全局按天慢查询总数
2. 全局按执行时长分布
3. 全局按执行时间分布
4. 实例按天慢查询变化
5. sql 格式化后聚合统计
6. topsql 按次数，时长，row排序

### 统计逻辑

1. 统计每小时进行一次，计算上一小时接受的慢查询信息。
2. 遍历数据集对每一个slowlog 进行解析，格式化，计算维度值（time,row,count）
3. 更新按实例统计维度表。slowlog_time_hour
3. 更新按天统计表


##数据表设计

	CREATE TABLE `slowlog_info` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `db_host` varchar(200) COLLATE utf8_bin DEFAULT NULL,
	  `port` int(11) DEFAULT NULL,
	  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	  `user` varchar(200) COLLATE utf8_bin DEFAULT NULL,
	  `user_host` varchar(200) COLLATE utf8_bin DEFAULT NULL,
	  `query_time` float(10,4) DEFAULT NULL,
	  `lock_time` float(10,4) DEFAULT NULL,
	  `rows_sent` int(11) DEFAULT NULL,
	  `rows_examined` int(11) DEFAULT NULL,
	  `sql_text` mediumtext COLLATE utf8_bin,
	  `sql_explained` mediumtext COLLATE utf8_bin,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_bin

##元数据
	
	Time: 140228 16:15:10
	User@Host: root[root] @  [127.0.0.1]  Id:    15
	Query_time: 2.201578  Lock_time: 0.000080 Rows_sent: 1170482  Rows_examined: 1170482
	use dm;
	SET	timestamp=1393575310;
	SELECT /*!40001 SQL_NO_CACHE */ * FROM `fct_dat_moto_sp_pay_day`;

执行计划：
	
	mysql> explain select * from user;
	+----+-------------+-------+------+---------------+------+---------+------+------+-------+
	| id | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra |
	+----+-------------+-------+------+---------------+------+---------+------+------+-------+
	|  1 | SIMPLE      | user  | ALL  | NULL          | NULL | NULL    | NULL |    7 |       |
	+----+-------------+-------+------+---------------+------+---------+------+------+-------+
	1 row in set (0.00 sec)

##规则说明
1.sql唯一性
	使用sql解析时的timestamp和sql一起生成一个hash，用于标识一类唯一的sql：
		     
	return hash(str(time.time())+str)
2.sql 解析

配置所有变量并替换为N。不区分类型。样例sql可通过hash值获取。
