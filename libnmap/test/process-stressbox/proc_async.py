#!/usr/bin/env python

from libnmap.process import NmapProcess
from time import sleep


nmap_proc = NmapProcess(targets="scanme.nmap.org", options="-sT")
nmap_proc.run_background()
while nmap_proc.is_running():
    nmaptask = nmap_proc.current_task
    if nmaptask:
        print("Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
                                                           nmaptask.status,  
                                                           nmaptask.etc,
                                                           nmaptask.progress))
    sleep(0.5)

print("rc: {0} output: {1}".format(nmap_proc.rc, nmap_proc.summary))
print(nmap_proc.stdout)
