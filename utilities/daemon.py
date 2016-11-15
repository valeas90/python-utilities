# -*- coding: utf-8 -*-
"""
***********************************************************************************************************************
                                                daemon.py

Generic daemon class. Must be subclassed and the run() method must be overwritten.

***********************************************************************************************************************
"""

import sys, os, time, atexit
from signal import SIGTERM

class Daemon(object):

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        """
		Class constructor. If the subclass needs its own constructor, in the subclass __init__ must be added the parent call.
		Use super(self.__class__, self).__init__(pidfile)
        """
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
		Two fork magic. The launching process is no longer vinculated with the daemon.
        """

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Unlink father process
        os.setsid()
        os.umask(0)

        # second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

		# Standar file descriptors are redirected
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # Writes the pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Starts the daemon
        """
		# Checks the pidfile in case the daemon is already running.
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "The pidfile %s already exists. Daemon running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stops the daemon
        """
        # Get the pid 
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "The pidfile %s doesn't exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return

        # Tries to kill the daemon
        try:
            while 1:
                os.kill(pid, SIGTERM)
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
        """
        Restarts the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
		This method must be overwritten.
		The method must be called after the start() or restart() has been called.
        """
