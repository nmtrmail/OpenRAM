#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys, os, re, shutil
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
import debug
import getpass


class openram_front_end_test(openram_test):

    def runTest(self):
        OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
        config_file = "{}/tests/configs/config_mem_char_func".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        debug.info(1, "Testing commandline characterizer script memchar.py with 2-bit, 16 word SRAM.")
        out_file = "testsram"
        out_path = "/tmp/testsram_{0}_{1}_{2}".format(OPTS.tech_name, getpass.getuser(), os.getpid())

        # make sure we start without the files existing
        if os.path.exists(out_path):
            shutil.rmtree(out_path, ignore_errors=True)
        self.assertEqual(os.path.exists(out_path), False)

        try:
            os.makedirs(out_path, 0o0750)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(out_path, 0o0750)

        # specify the same verbosity for the system call
        options = ""
        for i in range(OPTS.verbose_level):
            options += " -v"

        if OPTS.spice_name:
            options += " -s {}".format(OPTS.spice_name)

        if OPTS.tech_name:
            options += " -t {}".format(OPTS.tech_name)

        options += " -j 2"

        # Always perform code coverage
        if OPTS.coverage == 0:
            debug.warning("Failed to find coverage installation. This can be installed with pip3 install coverage")
            exe_name = "{0}/memchar.py ".format(OPENRAM_HOME)
        else:
            exe_name = "{0}{1}/memchar.py ".format(OPTS.coverage_exe, OPENRAM_HOME)
        config_name = "{0}/tests/configs/config_mem_char_func.py".format(OPENRAM_HOME)
        cmd = "{0} -n -o {1} -p {2} {3} {4} 2>&1 > {5}/output.log".format(exe_name,
                                                                          out_file,
                                                                          out_path,
                                                                          options,
                                                                          config_name,
                                                                          out_path)
        debug.info(1, cmd)
        os.system(cmd)

        # Make sure there is any .lib file
        import glob
        files = glob.glob('{0}/*.lib'.format(out_path))
        self.assertTrue(len(files)>0)

        # grep any errors from the output
        output_log = open("{0}/output.log".format(out_path), "r")
        output = output_log.read()
        output_log.close()
        self.assertEqual(len(re.findall('ERROR', output)), 0)
        self.assertEqual(len(re.findall('WARNING', output)), 0)

        # now clean up the directory
        if not OPTS.keep_temp:
            if os.path.exists(out_path):
                shutil.rmtree(out_path, ignore_errors=True)
            self.assertEqual(os.path.exists(out_path), False)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
