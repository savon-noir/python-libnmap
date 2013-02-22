#!/usr/bin/env python 
import pdb
import os, sys, shlex
from time import sleep
import subprocess
from threading  import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty
from xml.dom import pulldom

class NmapProcess:
    class ProcessState: 
       READY=1 
       RUNNING=2
       CANCELLED=3
       FAILED=4
       DONE=5

    def __init__(self, targets="127.0.0.1", options= "-sT", event_callback=None):
        self._nmap_proc = None
        self._nmap_rc = 0
        self._nmap_results = {}
 
        self._nmap_binary_name = "nmap"
        self._nmap_fixed_options = "-oX - -v --stats-every 5s"
        self._nmap_binary = self._whereis(self._nmap_binary_name)
        self._sudo_run = ""
        self.__process = self.ProcessState()

        self._nmap_targets = targets.split() if isinstance(targets, str) else targets
        self._nmap_dynamic_options = options

        self._nmap_command_line = self.get_command_line()
        self._nmap_event_callback = event_callback if event_callback and callable(event_callback) else None
        self.__io_queue = Queue()
        (self._stdin, self._stdout, self._stderr) = (None, None, None)
        self.state = self.__process.READY
        self.progress = 0
        self.etc = 0
        self.__blocking = True

    def _run_init(self):
        self._nmap_proc = None
        self._nmap_rc = 0
        self._nmap_results = {}
        self._nmap_command_line = self.get_command_line()
        self.state = self.__process.READY
        self.progress = 0
        self.etc = 0
        self.__blocking = True

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

    def start(self, blocking=True):
        def stdout_reader(thread_stdout, io_queue):
            for streamline in iter(thread_stdout.readline, b''):
                if streamline is not None: io_queue.put(streamline)

        rc = 0
        self._run_init()
        self._nmap_proc = subprocess.Popen(args=shlex.split(self._nmap_command_line), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        t = Thread(target=stdout_reader, args=(self._nmap_proc.stdout, self.__io_queue))
        t.daemon = True
        t.start()

        self.state = self.__process.RUNNING
        self.__wait = blocking

        return rc

    def wait(self):
        thread_output = ""
        while self._nmap_proc.poll() is None or not self.__io_queue.empty():
            try: thread_stream = self.__io_queue.get_nowait()
            except Empty: pass
            else:
                if self._nmap_event_callback: self._nmap_event_callback(thread_stream)
                self.process_event(thread_stream)
                thread_output += thread_stream
            sleep(500/1000000.0)

        self._nmap_rc = self._nmap_proc.poll()
        self._nmap_results = thread_output
        
        self.state = self.__process.DONE

        return self._nmap_rc

    def get_nowait(self):
        streamdata = ''
        if not self.__io_queue.empty():
           try:
               streamdata = self.__io_queue.get_nowait()
           except Empty: pass

        if self._nmap_proc.poll() is not None:
            self._nmap_rc = self._nmap_proc.poll()
            if self._nmap_rc == 0:
                rc = self.state == self.__process.DONE
            else:
                rc = self.state == self.__process.FAILED

        self.process_event(streamdata)

        return streamdata

    def is_running(self):
        rc = False
        if self.__wait:
            rc = self.state == self.__process.RUNNING
        elif self._nmap_proc.poll() is None and self.state == self.__process.RUNNING:
            rc = True
        return rc

    def is_done(self):
        rc = False
        if self.__wait:
            rc = self.state == self.__process.DONE
        elif self._nmap_proc.poll() is not None:
            if self.state == self.__process.RUNNING: 
                self.state == self.__process.DONE
            rc = True
        return rc

    def is_failed(self):
        return self.state == self.__process.FAILED

    def update_progress(self, percent_done, etc):
        self.progress = percent_done
        self.etc = etc

    def process_event(self, eventdata):
        try:
           edomdoc = pulldom.parseString(eventdata)
           for e, xmlnode in edomdoc:
               if e is not None and e == pulldom.START_ELEMENT and xmlnode.nodeName == 'taskprogress' and xmlnode.attributes.keys():
                   self.update_progress(xmlnode.attributes['percent'].value, xmlnode.attributes['etc'].value)
        except: pass

def main(argv):
    def mycallback(data): pass
        #print "XML SIZE: [%d]" % (len(data))

    nm = NmapProcess("scanme.nmap.org", event_callback=mycallback)
    #print nm.get_command_line()
    nm.start()
    rc = nm.wait()

    if rc == 0:
         print "results: %d" % len(nm._nmap_results)
    else:
         print "rc: %d" % rc
#
#    print "-----------------"
#    t = nm.start(blocking=False)
#    while nm.is_running():
#        s = nm.get_nowait()
#        if len(s):
#            print "%s%% %s" % (nm.progress, nm.etc)
#        sleep(2)
#
if __name__ == '__main__':
    main(sys.argv[1:])
