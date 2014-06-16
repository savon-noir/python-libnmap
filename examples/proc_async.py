#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.process import NmapProcess
from time import sleep


nmap_proc = NmapProcess(targets="scanme.nmap.org", options="-sT")
nmap_proc.run_background()
while nmap_proc.is_running():
    print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nmap_proc.etc,
                                                          nmap_proc.progress))
    sleep(2)

print("rc: {0} output: {1}".format(nmap_proc.rc, nmap_proc.summary))
