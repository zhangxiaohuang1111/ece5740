#=========================================================================
# csr: csrr mngr2proc/numcores/coreid and csrw proc2mngr/stats_en
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_asm_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x2, mngr2proc   < 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x2   > 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# gen_bypass_asm_test
#-------------------------------------------------------------------------

def gen_bypass_test():
  return """
    csrr x2, mngr2proc   < 0xdeadbeef
    {nops_3}
    csrw proc2mngr, x2   > 0xdeadbeef

    csrr x2, mngr2proc   < 0x00000eef
    {nops_2}
    csrw proc2mngr, x2   > 0x00000eef

    csrr x2, mngr2proc   < 0xdeadbee0
    {nops_1}
    csrw proc2mngr, x2   > 0xdeadbee0

    csrr x2, mngr2proc   < 0xde000eef
    csrw proc2mngr, x2   > 0xde000eef


    csrr x2, mngr2proc   < 0xdeadbeef
    csrw proc2mngr, x2   > 0xdeadbeef
    csrr x1, mngr2proc   < 0xcafecafe
    csrw proc2mngr, x1   > 0xcafecafe
  """.format(
    nops_3=gen_nops(3),
    nops_2=gen_nops(2),
    nops_1=gen_nops(1)
  )

#-------------------------------------------------------------------------
# gen_value_asm_test
#-------------------------------------------------------------------------

def gen_value_test():
  return """
    csrw proc2mngr, x0   > 0x00000000 # test r0 is always 0
    csrr x0, mngr2proc   < 0xabcabcff # even if we try to write r0
    csrw proc2mngr, x0   > 0x00000000
  """

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():

  asm_code = []
  for i in range(100):
    value = random.randint(0,0xffffffff)
    asm_code.append( """

      csrr x1, mngr2proc   < {value}
      csrw proc2mngr, x1   > {value}

    """.format( **locals() ))

  return asm_code

#-------------------------------------------------------------------------
# num_cores and core_id tests; turn on -s to see stats_on/off trace
#-------------------------------------------------------------------------

def gen_core_stats_test():
  return """

    # Turn on stats here
    csrr x1, mngr2proc < 1
    csrw stats_en, x1

    # Check numcores/coreid
    csrr x2, numcores
    csrw proc2mngr, x2 > 1
    csrr x2, coreid
    csrw proc2mngr, x2 > 0

    # Turn off stats here
    csrw stats_en, x0
    nop
    nop
    csrr x1, mngr2proc < 1
    csrw proc2mngr, x1 > 1
    nop
    nop
    nop
  """

