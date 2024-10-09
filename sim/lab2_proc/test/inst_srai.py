#=========================================================================
# srai
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
    srai x3, x1, 0x03
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
    gen_rimm_dest_dep_test( 5, "srai",  0x80000000,  1, 0xC0000000 ),   # -2147483648 >> 1 -> -1073741824
    gen_rimm_dest_dep_test( 4, "srai",  0x7FFFFFFF,  1, 0x3FFFFFFF ),   # 2147483647 >> 1 -> 1073741823
    gen_rimm_dest_dep_test( 3, "srai",  0x80000000,  31, 0xFFFFFFFF ),  # -2147483648 >> 31 -> -1
    gen_rimm_dest_dep_test( 2, "srai",  0x7FFFFFFF,  31, 0x00000000 ),  # 2147483647 >> 31 -> 0
    gen_rimm_dest_dep_test( 1, "srai",  0x40000000,  2, 0x10000000 ),   # 1073741824 >> 2 -> 268435456
    gen_rimm_dest_dep_test( 0, "srai",  0xFFFFFFFF,  4, 0xFFFFFFFF ),   # -1 >> 4 -> -1 (sign-extended)
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srai",  0x80000000,  1, 0xC0000000 ),   # -2147483648 >> 1 -> -1073741824
    gen_rimm_src_dep_test( 4, "srai",  0x7FFFFFFF,  1, 0x3FFFFFFF ),   # 2147483647 >> 1 -> 1073741823
    gen_rimm_src_dep_test( 3, "srai",  0x80000000,  31, 0xFFFFFFFF ),  # -2147483648 >> 31 -> -1
    gen_rimm_src_dep_test( 2, "srai",  0x7FFFFFFF,  31, 0x00000000 ),  # 2147483647 >> 31 -> 0
    gen_rimm_src_dep_test( 1, "srai",  0x40000000,  2, 0x10000000 ),   # 1073741824 >> 2 -> 268435456
    gen_rimm_src_dep_test( 0, "srai",  0xFFFFFFFF,  4, 0xFFFFFFFF ),   # -1 >> 4 -> -1
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "srai",  0x80000000, 1, 0xC0000000 ),
    gen_rimm_src_eq_dest_test( "srai",  0x7FFFFFFF, 1, 0x3FFFFFFF ),
    gen_rimm_src_eq_dest_test( "srai",  0xFFFFFFFF, 4, 0xFFFFFFFF ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    # Positive and negative values
    gen_rimm_value_test( "srai", 0x00000001, 0x01, 0x00000000 ),  # 1 >> 1 -> 0
    gen_rimm_value_test( "srai", 0x80000000, 0x01, 0xC0000000 ),  # -2147483648 >> 1 -> -1073741824
    gen_rimm_value_test( "srai", 0x7FFFFFFF, 0x01, 0x3FFFFFFF ),  # 2147483647 >> 1 -> 1073741823
    gen_rimm_value_test( "srai", 0x80000000, 0x1F, 0xFFFFFFFF ),  # -2147483648 >> 31 -> -1
    gen_rimm_value_test( "srai", 0x7FFFFFFF, 0x1F, 0x00000000 ),  # 2147483647 >> 31 -> 0
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = random.randint(0, 0xFFFFFFFF)
    imm = random.randint(0, 0x1F)  # Immediate is between 0 and 31 for shifts
    
    # Convert src to signed 32-bit integer to simulate arithmetic right shift
    if src & 0x80000000:
      src_signed = src - 0x100000000  # Convert unsigned to signed (2's complement)
    else:
      src_signed = src

    # Perform arithmetic right shift
    dest = src_signed >> imm

    # Convert back to unsigned 32-bit value to match the result of SRAI
    dest &= 0xFFFFFFFF

    asm_code.append( gen_rimm_value_test( "srai", src, imm, dest ) )
  
  return asm_code

