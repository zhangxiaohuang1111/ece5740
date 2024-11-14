#=========================================================================
# extra multicore memory tests
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < {0x00002000,0x00002004,0x00002008,0x0000200c}
    csrr x2, mngr2proc < {0x0a0b0c0d,0x1a1b1c1d,0x2a2b2c2d,0x3a3b3c3d}
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sw   x2, 0(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw   x3, 0(x1)
    csrw proc2mngr, x3 > {0x0a0b0c0d,0x1a1b1c1d,0x2a2b2c2d,0x3a3b3c3d}

    .data
    .word 0x01020304
    .word 0x11121314
    .word 0x21222324
    .word 0x31323334
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
