#!/usr/bin/python
# -*- coding: latin-1 -*-

## Quick hack of a marker tool for making lists of interesting events in project documentation
## Meant to be used when viewing session recordings, livesessions, etc
## 2016 Oeyvind Brandtsegg (obrandts@gmail.com)

import time

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen. From http://code.activestate.com/recipes/134892/"""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMacCarbon()
            except(AttributeError, ImportError):
                self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class _GetchMacCarbon:
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.  The
    page http://www.mactech.com/macintosh-c/chap02-1.html was
    very helpful in figuring out how to do this.
    """
    def __init__(self):
        import Carbon
        Carbon.Evt #see if it has this (in Unix, it doesn't)

    def __call__(self):
        import Carbon
        if Carbon.Evt.EventAvail(0x0008)[0]==0: # 0x0008 is the keyDownMask
            return ''
        else:
            #
            # The event contains the following info:
            # (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            #
            # The message (msg) contains the ASCII char which is
            # extracted with the 0x000000FF charCodeMask; this
            # number is converted to an ASCII character with chr() and
            # returned
            #
            (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)


def getKey():
    inkey = _Getch()
    import sys
    for i in xrange(sys.maxint):
        k=inkey()
        if k<>'':break
    return k
    
def isInt(v):
    try:     i = int(v)
    except:  return False
    return True
    
def time_add(t1, t2):
    h1,m1,s1 = t1.split(':')
    h2,m2,s2 = t2.split(':')
    sum_s = int(s1)+int(s2)
    mem_m = sum_s/60
    sum_s %= 60
    sum_m = int(m1)+int(m2)+mem_m
    mem_h = sum_m/60
    sum_m %= 60
    sum_h = int(h1)+int(h2)+mem_h
    return '{:02d}:{:02d}:{:02d}'.format(sum_h, sum_m, sum_s)

def update_running_time(t,timedelta):
    now = int(time.time())
    if t != now:
        inc = '00:00:{:02d}'.format(now-t)
        timedelta = time_add(timedelta, inc)
    return now, timedelta
        
def update_timedelta(t, timedelta):
    if (len(t) != 8) or (len(t.split(':')) != 3):
        print 'invalid time format, use hh:mm:ss format'
    else:
        timedelta = t
        print 'time delta set to {}'.format(t)
    return timedelta
    
if __name__=="__main__":
    run = 1
    runclock = 0
    time_0 = int(time.time())
    timedelta = '00:00:00'
    print '\n*** *** ***'
    print 'Enter markers by using number keys (0-9)'
    print 'The time marker will be set to N seconds before the time it was entered,'
    print '...using the number pressed as N\n'
    time.sleep(0.3)
    print 'Add a comment to the last marker by typing C (optional)'
    print 'Set the significance of the latest event marked by typing V (optional)'
    print 'Set the session sync time by typing T'
    print 'Start and stop the session sync time with the space bar'
    time.sleep(0.4)
    print 'Quit and save: type "_"'
    print '*** *** ***'
    start_timedate = time.strftime('%Y_%m_%d_%H_%M_%S')
    markerlist = []
    # marker format: localtime, synctime, significance, comment
    # where synctime is the time into the track, performance or other media/action
    # significance is the subjective immediate and approximate value if significance of the event (from 1 to 9)
    while run:
        key = getKey()
        if runclock > 0:
            time_0, timedelta = update_running_time(time_0, timedelta)
        if key == '_':
            run = 0
        elif isInt(key):
            print 'add marker {} seconds ago'.format(key)
            now = time.strftime('%H:%M:%S')
            predelay = '00:00:-{:02d}'.format(int(key))
            now = time_add(now,predelay)
            synctime = time_add(timedelta,predelay)
            print '    time: {}, synctime: {}'.format(now, synctime)
            markerlist.append([now,timedelta,' \t', ' '])
        elif key == ' ':
            runclock = (runclock+1)%2
            print 'clock running: {} at time {}'.format(runclock, timedelta)
            if runclock == 1:
                time_0 = int(time.time())
        elif key == 'T':
            print 'set time (hh:mm:ss)'
            t = raw_input()
            timedelta = update_timedelta(t, timedelta)
        elif key == 'C':
            print 'enter comment for last marker'
            comment = raw_input()
            markerlist[-1][3] = comment
        elif key == 'V':
            print 'enter marker significance (1-9)'
            val = raw_input()
            if isInt(val):
                markerlist[-1][2] = val+'\t'
        else:
            print 'key {} not used'.format(key)
    outfilename = 'marker_log_'+start_timedate+'.txt'
    f = open(outfilename, 'w')
    f.write('Marker file for Crossadaptive project\n')
    f.write('{} markers\n\n'.format(len(markerlist)))
    f.write('Time\t\tSynctime\tSignificance\tComment\n')
    for item in markerlist:
        s = ''
        for it in item:
            s += it+'\t'
        f.write(s +'\n')
    f.close()