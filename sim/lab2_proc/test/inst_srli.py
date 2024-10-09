#=========================================================================
# srli
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
    csrr x1, mngr2proc < 0x00008000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srli x3, x1, 0x03
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00001000
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
    gen_rimm_dest_dep_test( 5, "srli",  0xFFFFFFFF,  1, 0x7FFFFFFF ),   # Max value >> 1
    gen_rimm_dest_dep_test( 4, "srli",  0x00000001,  1, 0x00000000 ),   # 1 >> 1 -> 0
    gen_rimm_dest_dep_test( 3, "srli",  0x00000002,  1, 0x00000001 ),   # 2 >> 1 -> 1
    gen_rimm_dest_dep_test( 2, "srli",  0xFFFFFFFF, 31, 0x00000001 ),   # Max value >> 31
    gen_rimm_dest_dep_test( 1, "srli",  0x80000000,  1, 0x40000000 ),   # Sign bit >> 1 (logical, no sign extension)
    gen_rimm_dest_dep_test( 0, "srli",  0x7FFFFFFF,  1, 0x3FFFFFFF ),   # Positive max >> 1
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srli",  0xFFFFFFFF,  1, 0x7FFFFFFF ),   # Max value >> 1
    gen_rimm_src_dep_test( 4, "srli",  0x00000001,  1, 0x00000000 ),   # 1 >> 1 -> 0
    gen_rimm_src_dep_test( 3, "srli",  0x00000002,  1, 0x00000001 ),   # 2 >> 1 -> 1
    gen_rimm_src_dep_test( 2, "srli",  0xFFFFFFFF, 31, 0x00000001 ),   # Max value >> 31
    gen_rimm_src_dep_test( 1, "srli",  0x80000000,  1, 0x40000000 ),   # Sign bit >> 1 (logical)
    gen_rimm_src_dep_test( 0, "srli",  0x7FFFFFFF,  1, 0x3FFFFFFF ),   # Positive max >> 1
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "srli", 0xFFFFFFFF, 1, 0x7FFFFFFF ),   # Max value >> 1
    gen_rimm_src_eq_dest_test( "srli", 0x00000001, 1, 0x00000000 ),   # 1 >> 1 -> 0
    gen_rimm_src_eq_dest_test( "srli", 0x80000000, 1, 0x40000000 ),   # Sign bit >> 1 (logical)
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    # Positive and negative values
    gen_rimm_value_test( "srli", 0x00000001, 0x01, 0x00000000 ),  # 1 >> 1 -> 0
    gen_rimm_value_test( "srli", 0x80000000, 0x01, 0x40000000 ),  # Sign bit (logical) >> 1
    gen_rimm_value_test( "srli", 0x7FFFFFFF, 0x01, 0x3FFFFFFF ),  # Max positive >> 1
    gen_rimm_value_test( "srli", 0xFFFFFFFF, 0x1F, 0x00000001 ),  # Max value >> 31 -> 1
    gen_rimm_value_test( "srli", 0x80000000, 0x1F, 0x00000001 ),  # Sign bit >> 31 -> 0
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = random.randint(0, 0xFFFFFFFF)
    imm = random.randint(0, 0x1F)  # Immediate is between 0 and 31 for shifts

    # Perform logical right shift (append zeros on the left)
    dest = src >> imm

    # Append the test case to the list
    asm_code.append( gen_rimm_value_test( "srli", src, imm, dest ) )

  return asm_code