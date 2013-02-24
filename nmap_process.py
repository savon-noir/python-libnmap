#!/usr/bin/env python 
import os, sys, shlex
import time
import subprocess
from threading  import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty
from xml.dom import pulldom

class NmapProcess:
    def __init__(self, targets="127.0.0.1", options= "-sT", event_callback=None):
        self._nmap_proc = None
        self._nmap_rc = 0
        self._nmap_results = ''
 
        self._nmap_binary_name = "nmap"
        self._nmap_fixed_options = "-oX - -vvv --stats-every 2s"
        self._nmap_binary = self._whereis(self._nmap_binary_name)
        self._sudo_run = ""
        self._nmap_targets = targets.split() if isinstance(targets, str) else targets
        self._nmap_dynamic_options = options

        self._nmap_command_line = self.get_command_line()
        self._nmap_event_callback = event_callback if event_callback and callable(event_callback) else None
        self.__io_queue = Queue()
        (self._stdin, self._stdout, self._stderr) = (None, None, None)
        (self.DONE, self.READY, self.RUNNING, self.CANCELLED, self.FAILED) = range(5)

        # API usable in callback function
        self.state = self.READY
        self.starttime = 0
        self.endtime = 0 
        self.progress = 0
        self.etc = 0
        self.elapsed = ''
        self.summary = ''

    def _run_init(self):
        self._nmap_proc = None
        self._nmap_rc = -1
        self._nmap_results = ''
        self._nmap_command_line = self.get_command_line()
        self.state = self.READY
        self.progress = 0
        self.etc = 0
        self.starttime = 0
        self.endtime = 0
        self.elapsed = ''
        self.summary = ''

    def _whereis(self, program):
        for path in os.environ.get('PATH', '').split(':'):
            if os.path.exists(os.path.join(path, program)) and not os.path.isdir(os.path.join(path, program)):
                return os.path.join(path, program)
        return None

    def get_command_line(self):
        return "%s %s %s %s %s".lstrip() % (self._sudo_run, self._nmap_binary, self._nmap_fixed_options, self._nmap_dynamic_options, " ".join(self._nmap_targets))

    def set_command_line(self, targets, options='-sT'):
        self._nmap_targets = targets.split()
        self._nmap_dynamic_options = options
        self._nmap_command_line = self.get_command_line()

    def sudo_run(self, run_as='root'):
        self._sudo_run = "sudo -u %s" % (run_as)
        rc = self.run()
        self._sudo_run = ""

        return rc

    def run(self):
        def stdout_reader(thread_stdout, io_queue):
            for streamline in iter(thread_stdout.readline, b''):
                try:
                    if streamline is not None: io_queue.put(streamline)
                except Full: 
                    raise Exception("Queue ran out of buffer: increase q.get(timeout) value")

        self._run_init()
        try:
            self._nmap_proc = subprocess.Popen(args=shlex.split(self._nmap_command_line), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            t = Thread(target=stdout_reader, args=(self._nmap_proc.stdout, self.__io_queue))
            t.daemon = True
            t.start()

            self.state = self.RUNNING
        except OSError as e: # nmap not found
            self.state = self.FAILED
            raise

        return self.get()

    def get(self):
        thread_stream = ''
        while self._nmap_proc.poll() is None or not self.__io_queue.empty():
            try: thread_stream = self.__io_queue.get(timeout=1)
            except Empty: pass
            except KeyboardInterrupt: break
            else:
                if self._nmap_event_callback: self._nmap_event_callback(self, thread_stream)
                self.process_event(thread_stream)
                self._nmap_results += thread_stream

        self._nmap_rc = self._nmap_proc.poll()
        if not self._nmap_rc:
            rc = self.state = self.CANCELLED
        elif self._nmap_rc == 0:
            rc = self.state = self.DONE
            self.progress = 100
        else:
            rc = self.state = self.FAILED

        return self._nmap_rc

    def is_running(self):
        return self.state == self.RUNNING

    def has_terminated(self):
        return self.state == self.DONE or self.state == self.FAILED or self.state == self.CANCELLED

    def has_failed(self):
        return self.state == self.FAILED

    def is_successful(self):
        return self.state == self.DONE

    def update_progress(self, percent_done, etc):
        self.progress = percent_done
        self.etc = etc

    def process_event(self, eventdata):
        try:
           edomdoc = pulldom.parseString(eventdata)
           for e, xmlnode in edomdoc:
               if e is not None and e == pulldom.START_ELEMENT:
                   if xmlnode.nodeName == 'taskprogress' and xmlnode.attributes.keys():
                       self.update_progress(xmlnode.attributes['percent'].value, xmlnode.attributes['etc'].value)
                   elif xmlnode.nodeName == 'nmaprun' and xmlnode.attributes.keys():
                       self.starttime = xmlnode.attributes['start'].value
                       self.nmap_version = xmlnode.attributes['version'].value
                   elif xmlnode.nodeName == 'finished' and xmlnode.attributes.keys():
                       self.endtime = xmlnode.attributes['time'].value
                       self.elapsed = xmlnode.attributes['elapsed'].value
                       self.summary = xmlnode.attributes['summary'].value
        except: pass

def main(argv):
    def mycallback(nmapscan=None, data=""):
        if nmapscan.is_running():
            print "Progress: %s %% - ETC: %s" % (nmapscan.progress, nmapscan.etc)

    nm = NmapProcess("scanme.nmap.org localhost", event_callback=mycallback)
    rc = nm.run()

    print "Scan started {0} {1}".format(nm.starttime, nm.nmap_version)
    print "results: %d" % len(nm._nmap_results)
    print "Scand ended {0}: {1}".format(nm.endtime, nm.summary)
    print "state: %s" % nm.state

if __name__ == '__main__':
    main(sys.argv[1:])
