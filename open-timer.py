#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 main for linux
"""
__author__ = 'Xu, Yuan'


import sys
from daemon import Daemon

import webapp
from timecollector import TimeCollector


class TimerDaemon(Daemon):
    def run(self):
        timecollector = TimeCollector()
        timecollector.start()
        webapp.main()


def usage():
    print "usage: %s start|stop|restart|status" % ""  # sys.argv[0]

if __name__ == "__main__":
    daemon = TimerDaemon('/tmp/open-timer-daemon.pid',
                         stderr='/tmp/open-pytimer-stderr.log',
                         stdout='/tmp/open-pytimer-stdout.log')
    if len(sys.argv) == 1:
        daemon.start()
    elif len(sys.argv) == 2:
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
