#=========================================================================
# simple_test_template.py
#=========================================================================
# This is a simple test for running the same assembly code on different
# processor models (ProcFL, ProcBase, ProcAlt).

import pytest
from pymtl3 import *
from lab2_proc.test.harness import asm_test, run_test
from lab2_proc.ProcFL import ProcFL
from lab2_proc.ProcBase import ProcBase
from lab2_proc.ProcAlt import ProcAlt

@pytest.mark.parametrize("ProcType", [ProcFL, ProcBase, ProcAlt])
def test_simple(ProcType, cmdline_opts):
  # Define a simple assembly program
  prog = """
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """
  # Run the test for the specified processor type
  run_test(ProcType, prog, cmdline_opts=cmdline_opts)