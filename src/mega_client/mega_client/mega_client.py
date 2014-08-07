'''
Created on Jun 20, 2014

@author: xchliu
'''

import sys, os, time, atexit
app_path=os.path.dirname(sys.path[0])
sys.path.append(app_path)
from signal import SIGTERM
from mega_client.client_main import main as client_main
from setting import DAEMON_PID,DAEMON_LOG


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
        return
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
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = pf.readlines()
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart
        # Try killing the daemon process            
        try:
            while 1:
                for p in pid:
                    os.kill(int(p.strip()), SIGTERM)
                    time.sleep(0.1)
        except OSError, err:    
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)
        
    def restart(self):
        self.stop()
        self.start()
        
    def _run(self):
        '''
        Call the main service ,put the child pid into pid file
        '''
        child_pid=client_main()
        
        for pid in child_pid:
            file(self.pidfile,'a+').write("%s\n" % pid)
        
if __name__ == "__main__":
    daemon = Daemon(DAEMON_PID)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
