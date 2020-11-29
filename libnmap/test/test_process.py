#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
from time import sleep

from libnmap.objects.report import NmapReport
from libnmap.parser import NmapParser
from libnmap.process import NmapProcess


class TestNmapProcess(unittest.TestCase):
    def setUp(self):
        self.fdir = os.path.dirname(os.path.realpath(__file__))

    def test_exec_env(self):
        self.assertRaises(
            EnvironmentError,
            NmapProcess,
            targets="127.0.0.1",
            options="-sV",
            fqp="/usr/bin/does-not-exists",
        )

    def test_exec(self):
        nmapobj = NmapProcess(targets="127.0.0.1", options="-sP")
        rc = nmapobj.run()
        parsed = NmapParser.parse(nmapobj.stdout)
        self.assertEqual(rc, 0)
        self.assertGreater(len(nmapobj.stdout), 0)
        self.assertIsInstance(parsed, NmapReport)

    def test_exec_background(self):
        def make_nmproc_obj(targets, options):
            return NmapProcess(targets=targets, options=options)

        def start_all_bg(nmprocs):
            for nmp in nmprocs:
                nmp.run_background()

        def any_running(nmprocs):
            return any([nmp.is_running() for nmp in nmprocs])

        def summarize(nmprocs):
            for nmp in nmprocs:
                print("rc: {0} output: {1}".format(nmp.rc, len(nmp.stdout)))

        nb_targets = 10
        nm_target = "localhost"
        nm_opts = "-sP"

        nm_targets = [nm_target for i in range(nb_targets)]
        nm_procs = [make_nmproc_obj(t, nm_opts) for t in nm_targets]
        start_all_bg(nm_procs)

        while any_running(nm_procs):
            sleep(2)

        self.assertEqual(len(nm_procs), nb_targets)

        # total_size = 0
        # for i in range(len(nm_procs)):
        #     total_size += len(nm_procs[i].stdout)
        # self.assertEqual(
        #     int(total_size / len(nm_procs)), int(len(nm_procs[0].stdout))
        # )


if __name__ == "__main__":
    test_suite = ["test_exec_env", "test_exec", "test_exec_background"]
    suite = unittest.TestSuite(map(TestNmapProcess, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
