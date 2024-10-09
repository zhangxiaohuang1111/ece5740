#=========================================================================
# slli
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
    csrr x1, mngr2proc < 0x80008000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slli x3, x1, 0x03
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00040000
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
    gen_rimm_dest_dep_test( 5, "slli",  0x00000001, 1, 0x00000002 ),   # 1 << 1 -> 2
    gen_rimm_dest_dep_test( 4, "slli",  0x80000000, 1, 0x00000000 ),   # 0x80000000 << 1 -> 0
    gen_rimm_dest_dep_test( 3, "slli",  0x7FFFFFFF, 1, 0xFFFFFFFE ),   # 0x7FFFFFFF << 1 -> 0xFFFFFFFE
    gen_rimm_dest_dep_test( 2, "slli",  0x00000001, 31, 0x80000000 ),  # 1 << 31 -> 0x80000000
    gen_rimm_dest_dep_test( 1, "slli",  0xFFFFFFFF, 1, 0xFFFFFFFE ),   # 0xFFFFFFFF << 1 -> 0xFFFFFFFE
    gen_rimm_dest_dep_test( 0, "slli",  0x40000000, 2, 0x00000000 ),   # 0x40000000 << 2 -> 0 (overflow)
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slli",  0x00000001, 1, 0x00000002 ),   # 1 << 1 -> 2
    gen_rimm_src_dep_test( 4, "slli",  0x80000000, 1, 0x00000000 ),   # 0x80000000 << 1 -> 0
    gen_rimm_src_dep_test( 3, "slli",  0x7FFFFFFF, 1, 0xFFFFFFFE ),   # 0x7FFFFFFF << 1 -> 0xFFFFFFFE
    gen_rimm_src_dep_test( 2, "slli",  0x00000001, 31, 0x80000000 ),  # 1 << 31 -> 0x80000000
    gen_rimm_src_dep_test( 1, "slli",  0xFFFFFFFF, 1, 0xFFFFFFFE ),   # 0xFFFFFFFF << 1 -> 0xFFFFFFFE
    gen_rimm_src_dep_test( 0, "slli",  0x40000000, 2, 0x00000000 ),   # 0x40000000 << 2 -> 0 (overflow)
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "slli", 0x00000001, 1, 0x00000002 ),   # 1 << 1 -> 2
    gen_rimm_src_eq_dest_test( "slli", 0x80000000, 1, 0x00000000 ),   # 0x80000000 << 1 (overflow)
    gen_rimm_src_eq_dest_test( "slli", 0x00000001, 31, 0x80000000 ),  # 1 << 31
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    # Positive and negative values
    gen_rimm_value_test( "slli", 0x00000001, 1, 0x00000002 ),  # 1 << 1 -> 2
    gen_rimm_value_test( "slli", 0x80000000, 1, 0x00000000 ),  # 0x80000000 << 1 -> overflow
    gen_rimm_value_test( "slli", 0x7FFFFFFF, 1, 0xFFFFFFFE ),  # Max positive << 1
    gen_rimm_value_test( "slli", 0x00000001, 31, 0x80000000 ), # 1 << 31 -> sign bit set
    gen_rimm_value_test( "slli", 0x00000002, 30, 0x80000000 ), # 2 << 30 -> 0x80000000
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = random.randint(0, 0xFFFFFFFF)
    imm = random.randint(0, 0x1F)  # Immediate is between 0 and 31 for shifts

    # Perform logical left shift (append zeros on the right)
    dest = (src << imm) & 0xFFFFFFFF

    # Append the test case to the list
    asm_code.append( gen_rimm_value_test( "slli", src, imm, dest ) )

  return asm_code