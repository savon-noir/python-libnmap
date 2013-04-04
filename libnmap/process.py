#!/usr/bin/env python 
import os
import sys
import pwd
import shlex
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
        if self._nmap_binary is None:
            raise EnvironmentError(1, "nmap is not installed or could not be found in system path")
        
        self._sudo_run = ""
        self._nmap_targets = targets.split() if isinstance(targets, str) else targets
        self._nmap_dynamic_options = options

        self._nmap_command_line = self.get_command_line()
        if event_callback and callable(event_callback):
            self._nmap_event_callback = event_callback
        else:
            self._nmap_event_callback = None
        (self.DONE, self.READY, self.RUNNING, self.CANCELLED, self.FAILED) = range(5)

        # API usable in callback function
        self.state = self.READY
        self.starttime = 0
        self.endtime = 0 
        self.progress = 0
        self.etc = 0
        self.elapsed = ''
        self.summary = ''
        self.stdout = ''
        self.stderr = ''

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
        self.nmap_version = ''
        self.__io_queue = Queue()
        self.__ioerr_queue = Queue()
        self.stdout = ''
        self.stderr = ''

    def _whereis(self, program):
        for path in os.environ.get('PATH', '').split(':'):
            if os.path.exists(os.path.join(path, program)) and not os.path.isdir(os.path.join(path, program)):
                return os.path.join(path, program)
        return None

    def get_command_line(self):
        return "%s %s %s %s %s".lstrip() % (self._sudo_run, self._nmap_binary,
                                            self._nmap_fixed_options,
                                            self._nmap_dynamic_options,
                                            " ".join(self._nmap_targets))

    def set_command_line(self, targets, options='-sT'):
        self._nmap_targets = targets.split()
        self._nmap_dynamic_options = options
        self._nmap_command_line = self.get_command_line()

    def sudo_run(self, run_as='root'):
        sudo_user = run_as.split(" ").pop()
        try:
            s_uid = pwd.getpwnam(sudo_user).pw_uid
        except KeyError:
            raise

        sudo_path = self._whereis("sudo")
        if sudo_path is None:
            raise EnvironmentError(2, "sudo is not installed or could not be found in system path: cannot run nmap with sudo")

        self._sudo_run = "%s -u %s" % (sudo_path, sudo_user)
        rc = self.run()
        self._sudo_run = ""

        return rc

    def run(self):
        def stream_reader(thread_stdout, io_queue):
            for streamline in iter(thread_stdout.readline, b''):
                try:
                    if streamline is not None: io_queue.put(streamline)
                except Full: 
                    raise Exception("Queue ran out of buffer: increase q.get(timeout) value")

        self._run_init()
        try:
            self._nmap_proc = subprocess.Popen(args=shlex.split(self._nmap_command_line), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            tout = Thread(target=stream_reader, name='stdout-reader', args=(self._nmap_proc.stdout, self.__io_queue)).start()
            terr = Thread(target=stream_reader, name='stderr-reader', args=(self._nmap_proc.stderr, self.__ioerr_queue)).start()

            self.state = self.RUNNING
        except OSError as e: # nmap not found
            self.state = self.FAILED
            raise

        return self.wait()

    def wait(self):
        thread_stream = ''
        while self._nmap_proc.poll() is None or not self.__io_queue.empty():
            try:
                thread_stream = self.__io_queue.get(timeout=1)
            except Empty:
                pass
            except KeyboardInterrupt:
                break
            else:
                e = self.process_event(thread_stream)
                if self._nmap_event_callback and e:
                    self._nmap_event_callback(self, thread_stream)
                self._nmap_results += thread_stream

        self._nmap_rc = self._nmap_proc.poll()
        if self._nmap_rc is None:
            rc = self.state = self.CANCELLED
        elif self._nmap_rc == 0:
            rc = self.state = self.DONE
            self.progress = 100
        else:
            rc = self.state = self.FAILED
            self.stderr = self.__ioerr_queue.get(timeout=2) 
        self.stdout = self._nmap_results

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
        rval = False
        try:
           edomdoc = pulldom.parseString(eventdata)
           for e, xmlnode in edomdoc:
               if e is not None and e == pulldom.START_ELEMENT:
                   if xmlnode.nodeName == 'taskprogress' and xmlnode.attributes.keys():
                       self.update_progress(xmlnode.attributes['percent'].value, xmlnode.attributes['etc'].value)
                       rval = True
                   elif xmlnode.nodeName == 'nmaprun' and xmlnode.attributes.keys():
                       self.starttime = xmlnode.attributes['start'].value
                       self.nmap_version = xmlnode.attributes['version'].value
                       rval = True
                   elif xmlnode.nodeName == 'finished' and xmlnode.attributes.keys():
                       self.endtime = xmlnode.attributes['time'].value
                       self.elapsed = xmlnode.attributes['elapsed'].value
                       self.summary = xmlnode.attributes['summary'].value
                       rval = True
        except: pass
        return rval

def main(argv):
    def mycallback(nmapscan=None, data=""):
        if nmapscan.is_running():
            print "Progress: %s %% - ETC: %s" % (nmapscan.progress, nmapscan.etc)

    nm = NmapProcess("localhost", options="-sT", event_callback=mycallback)
    rc = nm.run()

    if rc == 0:
        print "Scan started {0} {1}".format(nm.starttime, nm.nmap_version)
        print "results size: {0}".format(len(nm._nmap_results))
        print "Scan ended {0}: {1}".format(nm.endtime, nm.summary)
        print "state: %s" % nm.state
    else:
        print "Error: {stderr}".format(stderr=nm.stderr)
        print "Result: {0}".format(nm.stdout)

if __name__ == '__main__':
    main(sys.argv[1:])
