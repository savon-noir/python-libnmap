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
        if int(sys.version[0]) == 3:
            self._assertRaisesRegex = self.assertRaisesRegex
        else:
            self._assertRaisesRegex = self.assertRaisesRegexp
        self.fdir = os.path.dirname(os.path.realpath(__file__))

    def test_check_targets(self):
        invalid_target_tests = [{"a": "bba"}, 5]
        valid_target_tests = [
            {"value": "127.0.0.1, 1.1.1.1,     2.20.202", "size": 3},
            {"value": ["127.0.0.1", "1.1.1.1", "2.20.202.2"], "size": 3},
            {"value": ["     127.0.0.1", "  1.1.1.1"], "size": 2},
            {"value": "     127.0.0.1,      1.1.1.1  , a", "size": 3},
        ]
        for vtarget in valid_target_tests:
            nmapobj = NmapProcess(targets=vtarget["value"], options="-sP")
            self.assertEqual(vtarget["size"], len(nmapobj.targets))

        for vtarget in invalid_target_tests:
            self._assertRaisesRegex(
                Exception,
                "Supplied target list should be either a string or a list",
                NmapProcess,
                targets=vtarget,
                options="-sP",
            )

    def test_nmap_options(self):
        invalid_options = ["--iflist"]

        for invalid_option in invalid_options:
            self._assertRaisesRegex(
                Exception,
                "unsafe options activated while safe_mode is set True",
                NmapProcess,
                targets="127.0.0.1",
                options=invalid_option,
            )

    def test_missing_binary(self):
        _path = os.environ["PATH"]
        os.environ["PATH"] = "/does_not_exists"
        self._assertRaisesRegex(
            EnvironmentError,
            "nmap is not installed or could not be found in system path",
            NmapProcess,
            targets="127.0.0.1",
            options="-sP",
        )
        os.environ["PATH"] = _path

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

    def test_exec_reportsize(self):
        def make_nmproc_obj(targets, options):
            return NmapProcess(targets=targets, options=options)

        def start_all(nmprocs):
            for nmp in nmprocs:
                nmp.run()

        nb_targets = 20
        nm_target = "localhost"
        nm_opts = "-sT"

        nm_targets = [nm_target for i in range(nb_targets)]
        nm_procs = [make_nmproc_obj(t, nm_opts) for t in nm_targets]
        start_all(nm_procs)

        nm_procs = [make_nmproc_obj(t, nm_opts) for t in nm_targets]
        start_all(nm_procs)

        self.assertEqual(len(nm_procs), nb_targets)

        total_size = 0
        for i in range(len(nm_procs)):
            total_size += len(nm_procs[i].stdout)

        average_size = int(total_size / len(nm_procs))
        for nm in nm_procs:
            self.assertAlmostEqual(
                average_size, int(len(nm.stdout)), delta=200
            )


if __name__ == "__main__":
    test_suite = [
        "test_exec_env",
        "test_check_targets",
        "test_exec",
        "test_exec_reportsize",
    ]
    suite = unittest.TestSuite(map(TestNmapProcess, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
