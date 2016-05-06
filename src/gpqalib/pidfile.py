import sys
import os
import datetime
import subprocess
import time
import socket


def writelog(message):
    sys.stdout.write ('[%s PID %7d] %s\n' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), os.getpid(), message))
    sys.stdout.flush()
    return


def getpid(filename):
    res = -1
    try:
        if os.access(filename, os.F_OK):
            pidfile = open(filename, 'r')
            old_pid = pidfile.readline()
            if int(old_pid) != os.getpid() and os.path.exists("/proc/%s" % old_pid):
                res = int(old_pid)
    except Exception, ex:
        writelog('ERROR: Caught exception reading pidfile:')
        writelog('ERROR: %s' % str(ex))
    return res


def checkpid(filename):
    res = "occupied"
    try:
        if not os.access(filename, os.F_OK):
            res = "no file"
        else:
            pidfile = open(filename, 'r')
            old_pid = pidfile.readline()
            if int(old_pid) == os.getpid():
                res = "my lock"
            else:
                if not os.path.exists("/proc/%s" % old_pid):
                    res = "dead process"
    except Exception, ex:
        writelog('ERROR: Caught exception reading pidfile:')
        writelog('ERROR: %s' % str(ex))
        res = 'exception'
    return res


def writepid(filename):
    try:
        writelog ('Creating pid file "%s"' % filename)
        pidfile = open(filename, 'w')
        pidfile.write(str(os.getpid()))
        pidfile.close()
    except:
        pass
    return


def pidlock(filename):
    status = checkpid(filename)
    writelog('PID File Status: %s' % status)
    if status in ('no file', 'dead process'):
        writepid(filename)
    status = checkpid(filename)
    if status != 'my lock':
        writelog('WARNING: Cannot obtain lock. Status: %s' % status)
    return status


def pidrelease(filename):
    try:
        writelog ('Releasing pid file "%s"' % filename)
        os.remove(filename)
    except Exception, ex:
        writelog('WARNING: Caught exception removing pidfile:')
        writelog('WARNING: %s' % str(ex))
        pass
    return