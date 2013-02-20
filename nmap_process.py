#!/usr/bin/env python 
import os, sys, shlex
import subprocess
from threading  import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

class NmapProcess:
    class ProcessState: 
       READY=1 
       RUNNING=2 
       CANCELLED=3
       DONE=4

    def __init__(self, targets="127.0.0.1", options= "-sT", event_callback=None):
       self._nmap_proc = None
       self._nmap_rc = 0
       self._nmap_results = {}
       self._nmap_binary_name = "nmap"
       self._nmap_fixed_options = "-oX - -v"
       self._nmap_binary = self._whereis(self._nmap_binary_name)
       self._sudo_run = ""
       self.__process = self.ProcessState()

       self._nmap_targets = targets.split() if isinstance(targets, str) else targets
       self._nmap_dynamic_options = options

       self._nmap_command_line = self.get_command_line()
       self._nmap_event_callback = event_callback if event_callback and callable(event_callback) else None
       (self._stdin, self._stdout, self._stderr) = (None, None, None)
       self.state = self.__process.READY

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
                io_queue.put(streamline)

        io_queue = Queue()
        self._nmap_results = {}
        self._nmap_rc = 0
        self._nmap_proc = subprocess.Popen(args=shlex.split(self._nmap_command_line), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        t = Thread(target=stdout_reader, args=(self._nmap_proc.stdout, io_queue))
        t.daemon = True
        t.start()

        self.state = self.__process.RUNNING

        thread_output = ""
        while self._nmap_proc.poll() is None:
            try:  thread_stream = io_queue.get_nowait()
            except Empty: pass
            else:
                if self._nmap_event_callback: self._nmap_event_callback(thread_stream)
                thread_output += thread_stream

        self._nmap_rc = self._nmap_proc.poll()
        self._nmap_results = thread_output
        
        self.state = self.__process.DONE
        return self._nmap_rc


def main(argv):
 #   nm = NmapScan("localhost")
    def mycallback(data):
        print "XML SIZE: [%d] %s" % (len(data), data)
    nm = NmapProcess("scanme.nmap.org localhost", event_callback=mycallback)
    print nm.get_command_line()
    nm.run()
    #print "results: %s" % (nm._nmap_results)

if __name__ == '__main__':
    main(sys.argv[1:])
