#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 main for linux
"""
__author__ = 'Xu, Yuan'


import sys
from daemon import Daemon
import tray


class PyTimerDaemon(Daemon):
    def run(self):
        tray.main()


def usage():
    print "usage: %s start|stop|restart|status" % ""  # sys.argv[0]

if __name__ == "__main__":
    daemon = PyTimerDaemon('/tmp/pytimer-daemon.pid',
                            stderr='/tmp/pytimer-stderr.log',
                            stdout='/tmp/pytimer-stdout.log')
    if len(sys.argv) == 2:
        try:
            eval('daemon.' + sys.argv[1] + '()')
        except AttributeError:
            print "Unknown command"
            usage()
            sys.exit(2)
        sys.exit(0)
    else:
        usage()
        sys.exit(2)