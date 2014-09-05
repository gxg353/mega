#!/usr/bin/env python
'''
Created on Jun 20, 2014

@author: xchliu
'''

import sys, os, time, atexit
app_path=os.path.dirname(sys.path[0])
sys.path.append(app_path)
from signal import SIGTERM
from setting import DAEMON_PID,DAEMON_LOG,SERVICE_PID
from logs import Logger


MODEL='Daemon'
log = Logger(MODEL).log()



class Daemon:
    def __init__(self, pidfile, stderr=DAEMON_LOG, stdout=DAEMON_LOG, stdin='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def _daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        os.setsid()
        os.chdir("/")
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
        
    def delpid(self):
        os.remove(self.pidfile)
    #===========================================================================
    # start
    #===========================================================================
    def start(self):
        
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = pf.read().strip()
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        # Start the daemon
        self._daemonize()
        self._run()
        
    def stop(self):
        self._kill_pid(self.pidfile)
        self._kill_pid(SERVICE_PID)
        sub_process=os.popen("ps aux |grep python |grep  mega_client |grep -E 'start|restart' |grep -v grep |awk {'print $2'}").read().strip()
        try:
            for process in sub_process.split():
                log.debug("Process %s killed" % process)
                os.kill(int(process.strip()), SIGTERM)
        except OSError, err:    
            log.error(err)        
            
    def restart(self):
        self.stop()
        time.sleep(5)
        self.start()
    
    def upgrade(self):
        self._kill_pid(SERVICE_PID)
        
    def _run(self):
        '''
        Call the main service ,put the child pid into pid file
        loop : try to restart mega_client service if the subprocesses exit
        '''
        
        while 1:
            process_count=os.popen("ps aux |grep python |grep mega_client |grep -v grep |wc -l").read().strip()
            if int(process_count) < 3:
                #try to kill the sub process 
                self._kill_pid(SERVICE_PID)
                #import the main module
                client=__import__('client_main')
                client_main=getattr(client,'main')
                #wait for the subprocess exit
                pids=client_main(SERVICE_PID)
                log.debug(pids)
                f=open(SERVICE_PID,'w+')
                for pid in pids:
                    f.write("%s\n" % pid)
                f.close()
                log.debug("daemon loop end!")
            time.sleep(10)

    def _kill_pid(self,pidfile):
        if not os.path.exists(pidfile):
            return 
        try:
            pf = file(pidfile,'r')
            pid = pf.readlines()
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % pidfile)
            return # not an error in a restart
        # Try killing the daemon process            
        try:
            for p in pid:
                log.debug('Process %s killed' % p.strip())
                os.kill(int(p.strip()), SIGTERM)
        except OSError, err:    
            log.error(err)
        if os.path.exists(pidfile):
            os.remove(pidfile)

        return 
        
if __name__ == "__main__":
    daemon = Daemon(DAEMON_PID)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'upgrade' == sys.argv[1]:
            daemon.upgrade()
        else:
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|upgrade" % sys.argv[0]
        sys.exit(2)
