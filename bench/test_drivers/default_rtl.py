import sys
import os
import subprocess
import glob
import imp
import re

import dut_wrapper.soc as soc_lib
import benchlibs.debug as debug
import runner_checks as rchecks

from benchlibs.image_loader import ImageLoader

def run(libbench, opts, runner_override = None):

  soc = soc_lib.RiscVSoc(libbench, 'memtest_trace.vcd', True)
  soc.setDebug(False)

  ImageLoader.load_image("test.v", soc)

  if runner_override:
    print "custom runner procedure detected, control transfered"
    return driver.run(libbench, soc)

  print "could not detect custom runner procedure, using standard procedure"

  dbg = debug.Debugger(libbench, soc)

  if opts.ticks_limit == 0:
    print 'no ticks_limit specified, getting limit from the SOC object'
    opts.ticks_limit = soc.get_ticks_to_run()
    print 'new ticks_limit: {}'.format(opts.ticks_limit)

  if sys.stdout.isatty() or opts.enforce_repl:
    print('TTY session detected! starting debugger')

  # Unbuffer output (this ensures the output is in the correct order)
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

    tee = subprocess.Popen(["tee", "log.txt"], stdin=subprocess.PIPE)
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
    os.dup2(tee.stdin.fileno(), sys.stderr.fileno())

    dbg.set_tracing_enabled(True)
    dbg.repl()
  else:
    soc.run(opts.ticks_limit, expect_failure = opts.expect_failure)
    print("Working directory: {}".format(os.getcwd()))
    rchecks.RunnerChecks().check_uart('io.txt')

