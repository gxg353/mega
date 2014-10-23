
#Created on Jul 7, 2014

@author: xchliu

## 备份重复发起
由于时间临界点问题，导致一个备份在一次调用中2次运行，上一分钟59秒tracker 获取任务，下一秒进入api调用时使用下一分钟时间，则造成2次调用

修复：
	
	tracker 获取任务并获取当前时间，作为参数传送给具体参数
	    def backuper(self,now=None):
        '''
        retrun the server list which need to run backup right now
        '''
        if not now:
            now=time.strftime('%H:%M',time.localtime(time.time()))
        server_list = self.get_task(now)
        return server_list


