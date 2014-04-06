#!/usr/bin/env python
 
from libnmap.process import NmapProcess
from time import sleep
 
def make_nmproc_obj(targets, options):
    return NmapProcess(targets=targets, options=options)
 
def start_all(nmprocs):
    for nmp in nmprocs:
        print("Starting scan for host {0}".format(nmp.targets))
        nmp.run()
 
def summarize(nmprocs):
    for nmp in nmprocs:
        print "rc: {0} output: {1}".format(nmp.rc, nmp.summary)
 
nm_targets = ["localhost", "localhost", "localhost"]
nm_opts = "-sT"
 
nm_procs = [make_nmproc_obj(t, nm_opts) for t in nm_targets]
start_all(nm_procs)
 
summarize(nm_procs)
