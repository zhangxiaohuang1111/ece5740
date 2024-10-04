#=========================================================================
# slti
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slti x3, x1, 6
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 10
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slti x3, x1, 11
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 5, "slti",  10,  20, 1 ),
    gen_rimm_dest_dep_test( 4, "slti",  20,  10, 0 ),
    gen_rimm_dest_dep_test( 3, "slti", -10,   0, 1 ),
    gen_rimm_dest_dep_test( 2, "slti",   0, (-5) & 0xfff, 0 ),
    gen_rimm_dest_dep_test( 1, "slti", -20, (-10) & 0xfff, 1 ),
    gen_rimm_dest_dep_test( 0, "slti", -10, (-20) & 0xfff, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slti",  10,  20, 1 ),
    gen_rimm_src_dep_test( 4, "slti",  20,  10, 0 ),
    gen_rimm_src_dep_test( 3, "slti", -10,   0, 1 ),
    gen_rimm_src_dep_test( 2, "slti",   0, (-5) & 0xfff, 0 ),
    gen_rimm_src_dep_test( 1, "slti", -20, (-10) & 0xfff, 1 ),
    gen_rimm_src_dep_test( 0, "slti", -10, (-20) & 0xfff, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "slti",  10,  20, 1 ),
    gen_rimm_src_eq_dest_test( "slti",  -5,   5, 1 ),
    gen_rimm_src_eq_dest_test( "slti",  -1, (-1) & 0xfff, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "slti", 0x7FFFFFFF, (-1) & 0xfff, 0 ), # 2147483647 < -1 -> False
    gen_rimm_value_test( "slti", 0x80000000, 0, 1 ),            # -2147483648 < 0 -> True
    gen_rimm_value_test( "slti", -1, (-1) & 0xfff, 0 ),         # -1 < -1 -> False
    gen_rimm_value_test( "slti", 0, 0, 0 ),                     # 0 < 0 -> False
    gen_rimm_value_test( "slti", -5, (-5) & 0xfff, 0 ),         # -5 < -5 -> False
    gen_rimm_value_test( "slti", -5, 5, 1 ),                    # -5 < 5 -> True
    gen_rimm_value_test( "slti", 5, (-5) & 0xfff, 0 ),          # 5 < -5 -> False
    gen_rimm_value_test( "slti", 0x0000FFFF, 0xFFF, 0 ),        # 65535 < 4095 -> False
    gen_rimm_value_test( "slti", 0xFFFFFFFF, 1, 1 ),            # -1 < 1 -> True
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = random.randint(-2**31, 2**31 - 1)
    imm_raw = random.randint(0, 0xfff)
    imm = sext( Bits12(imm_raw), 32 ).int()
    dest = 1 if src < imm else 0
    asm_code.append( gen_rimm_value_test( "slti", src & 0xFFFFFFFF, imm_raw, dest ) )
  return asm_code

