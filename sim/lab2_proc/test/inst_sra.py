#=========================================================================
# sra
#=========================================================================

import random
import ctypes

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
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sra x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "sra", 0x80000000, 1, 0xC0000000 ),
    gen_rr_dest_dep_test( 4, "sra", 0x80000000, 2, 0xE0000000 ),
    gen_rr_dest_dep_test( 3, "sra", 0x80000000, 3, 0xF0000000 ),
    gen_rr_dest_dep_test( 2, "sra", 0x80000000, 4, 0xF8000000 ),
    gen_rr_dest_dep_test( 1, "sra", 0x80000000, 5, 0xFC000000 ),
    gen_rr_dest_dep_test( 0, "sra", 0x80000000, 31, 0xFFFFFFFF ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sra", 0x7FFFFFFF, 1, 0x3FFFFFFF ),
    gen_rr_src0_dep_test( 4, "sra", 0x7FFFFFFF, 2, 0x1FFFFFFF ),
    gen_rr_src0_dep_test( 3, "sra", 0x7FFFFFFF, 3, 0x0FFFFFFF ),
    gen_rr_src0_dep_test( 2, "sra", 0x7FFFFFFF, 4, 0x07FFFFFF ),
    gen_rr_src0_dep_test( 1, "sra", 0x7FFFFFFF, 5, 0x03FFFFFF ),
    gen_rr_src0_dep_test( 0, "sra", 0x7FFFFFFF, 31, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sra", 0xFFFFFFFF, 1, 0xFFFFFFFF ),
    gen_rr_src1_dep_test( 4, "sra", 0xFFFFFFFF, 2, 0xFFFFFFFF ),
    gen_rr_src1_dep_test( 3, "sra", 0xFFFFFFFF, 3, 0xFFFFFFFF ),
    gen_rr_src1_dep_test( 2, "sra", 0x0000FFFF, 4, 0x00000FFF ),
    gen_rr_src1_dep_test( 1, "sra", 0xFFFFFFFF, 5, 0xFFFFFFFF ),
    gen_rr_src1_dep_test( 0, "sra", 0xFFFFFFFF, 31, 0xFFFFFFFF ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sra", 0x00000008, 1, 0x00000004 ),
    gen_rr_srcs_dep_test( 4, "sra", 0x00000010, 2, 0x00000004 ),
    gen_rr_srcs_dep_test( 3, "sra", 0x00000020, 3, 0x00000004 ),
    gen_rr_srcs_dep_test( 2, "sra", 0x00000040, 4, 0x00000004 ),
    gen_rr_srcs_dep_test( 1, "sra", 0x00000080, 5, 0x00000004 ),
    gen_rr_srcs_dep_test( 0, "sra", 0xFFFFFFF0, 4, 0xFFFFFFFF ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sra", 0x80000000, 1, 0xC0000000 ),
    gen_rr_src1_eq_dest_test( "sra", 0x80000000, 1, 0xC0000000 ),
    gen_rr_src0_eq_src1_test( "sra", 1, 0x00000000 ),
    gen_rr_srcs_eq_dest_test( "sra", 4, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    # Test shifting positive numbers
    gen_rr_value_test( "sra", 0x7FFFFFFF, 0, 0x7FFFFFFF ),
    gen_rr_value_test( "sra", 0x7FFFFFFF, 1, 0x3FFFFFFF ),
    gen_rr_value_test( "sra", 0x7FFFFFFF, 31, 0x00000000 ),
    # Test shifting negative numbers
    gen_rr_value_test( "sra", 0x80000000, 0, 0x80000000 ),
    gen_rr_value_test( "sra", 0x80000000, 1, 0xC0000000 ),
    gen_rr_value_test( "sra", 0x80000000, 31, 0xFFFFFFFF ),
    # Test shifting zero
    gen_rr_value_test( "sra", 0x00000000, 0, 0x00000000 ),
    gen_rr_value_test( "sra", 0x00000000, 1, 0x00000000 ),
    gen_rr_value_test( "sra", 0x00000000, 31, 0x00000000 ),
    # Test maximum shift amount
    gen_rr_value_test( "sra", 0x12345678, 31, 0x00000000 ),
    gen_rr_value_test( "sra", 0xFFFFFFFF, 31, 0xFFFFFFFF ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = random.randint(0, 0xFFFFFFFF)
    src1 = random.randint(0, 31)
    # Interpret src0 as signed 32-bit integer
    src0_signed = ctypes.c_int32(src0).value
    # Perform arithmetic right shift
    dest = src0_signed >> src1
    # Ensure dest is in 32-bit signed integer range
    dest &= 0xFFFFFFFF
    asm_code.append( gen_rr_value_test( "sra", src0, src1, dest ) )
  return asm_code
