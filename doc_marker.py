#!/usr/bin/python
# -*- coding: latin-1 -*-

## Quick hack of a marker tool for making lists of interesting events in project documentation
## Meant to be used when viewing session recordings, livesessions, etc
## 2016-17 Oeyvind Brandtsegg (obrandts@gmail.com)

from Tkinter import *
import time
start_timedate = time.strftime('%Y_%m_%d_%H_%M_%S')

master = Tk()
i = 2
timewidth = 8
stimewidth = 10
signwidth = 10
commentwidth = 40
alt = False
latest_significance = ''
latest_comment = ''
master_list = []

def setalt(event):
    global alt
    alt = True
    
def key(event):
    global alt
    try:
        key = int(event.char)
    except:
        key = event.char
    if alt and key in range(10):
        global i, latest_significance,latest_comment, master_list
        tim, stim, signi, comm, latest_significance, latest_comment = make_event(master, i, event.char)
        master_list.append([tim, stim, signi, comm])
        i += 1
    if alt and key == 's':
        latest_significance.focus()
    if alt and key == 'c':
        latest_comment.focus()
    alt = False
        
def make_event(parent, linenum, preroll=0):
    t = StringVar()
    tim = Entry(master, textvariable=t, width=timewidth)
    tim.grid(row=linenum, column=0)
    t.set(clock_add(time1, -int(preroll)))
    s = StringVar()
    stim = Entry(master, textvariable=s, width=stimewidth)
    stim.grid(row=linenum, column=1)
    s.set(clock_add(synctime1, -int(preroll)))
    signi= StringVar()
    significance = Entry(master, textvariable=signi, width=signwidth)
    significance.grid(row=linenum, column=2)
    comm = StringVar()
    comment = Entry(master, textvariable=comm, width=commentwidth)
    comment.grid(row=linenum, column=3)
    return t, s, signi,comm, significance, comment

def tick():
    global time1, synctime1, sync_reftime
    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    timenow = int(time.time())
    if t_btn.config('text')[-1] == 'Sync: running':
        if sync_reftime < timenow:
            addtime = timenow-sync_reftime
            synctime1 = clock_add(synctime1, addtime)
            sync_reftime = int(time.time())
            synctime1var.set(synctime1)
    clock.after(200, tick)

def clock_add(t, add_n):
    t1 = t.split(':')
    t1[-1] = int(t1[-1])+add_n
    t1[-2] = int(t1[-2])+(t1[-1]/60)
    t1[-3] = int(t1[-3])+(t1[-2]/60)
    t1[-1] %= 60
    t1[-2] %= 60
    t1[-3] %= 24
    return '{0:02d}:{1:02d}:{2:02d}'.format(*t1)

def toggle():
    if t_btn.config('text')[-1] == 'Sync: running':
        t_btn.config(text='Sync: stopped')
    else:
        t_btn.config(text='Sync: running')
        global sync_reftime
        sync_reftime = int(time.time())

def enter_new_synctime(event):
    global synctime1var, sync_reftime,synctime1,syncclock,synctime1var_saved
    synctime1var.set(synctime1var.get())
    synctime1 = synctime1var.get()
    synctime1var_saved = synctime1var.get()
    syncclock.config(background='green')
    sync_reftime = synctime1var.get()

time1 = ''
clock = Label(master)
clock.grid(row=0, column=0)

synctime1 = '00:00:00'
sync_reftime = int(time.time())
synctime1var = StringVar()
synctime1var.set(synctime1)
synctime1var_saved = synctime1var.get()
syncclock = Entry(master, width=9, textvariable=synctime1var)
syncclock.grid(row=0, column=1)

t_btn = Button(text="Sync: stopped", width=12, command=toggle)
t_btn.grid(row=0, column=2)

Label(master, text="Time", width=timewidth).grid(row=1, column=0)
Label(master, text="Synctime", width=stimewidth).grid(row=1, column=1)
Label(master, text="Significance", width=signwidth).grid(row=1, column=2)
Label(master, text="Comment", width=commentwidth).grid(row=1, column=3)

def syncclock_edit(event):
    global syncclock
    syncclock.config(background='red')
    
master.bind("<Key>", key)
syncclock.bind("<Key>", syncclock_edit)
syncclock.bind("<Return>", enter_new_synctime)
master.bind("<Alt_L>", setalt)
tick()

mainloop()

outfilename = 'marker_log_'+start_timedate+'.txt'
f = open(outfilename, 'w')
f.write('Marker file for Crossadaptive project\n')
f.write('{} markers\n\n'.format(len(master_list)))
f.write('Synctime is {}\n\n'.format(synctime1var_saved))
f.write('Time\t\tSynctime\tSignificance\tComment\n')
for item in master_list:
    print('*\n')
    s = ''
    for e in item:
        s = s + e.get() + '\t'
    f.write(s +'\n')
    print(s)
f.close()
print('done')