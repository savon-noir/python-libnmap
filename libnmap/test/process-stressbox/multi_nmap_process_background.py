#!/usr/bin/env python
 
from libnmap.process import NmapProcess
from time import sleep
 
def make_nmproc_obj(targets, options):
  return NmapProcess(targets=targets, options=options)
 
def start_all_bg(nmprocs):
  for nmp in nmprocs: nmp.run_background()
 
def any_running(nmprocs):
  return any([nmp.is_running() for nmp in nmprocs])
 
def summarize(nmprocs):
  for nmp in nmprocs:
      print("rc: {0} output: {1} stdout len: {2}".format(nmp.rc, nmp.summary, len(nmp.stdout)))

nm_targets = []
for h in range(10):
    nm_targets.append("localhost")
nm_opts = "-sT"
 
nm_procs = [make_nmproc_obj(t, nm_opts) for t in nm_targets]
start_all_bg(nm_procs)
 
while any_running(nm_procs):
    print("Nmap Scan running...")
    sleep(2)
 
summarize(nm_procs)
