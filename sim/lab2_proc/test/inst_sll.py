#=========================================================================
# sll
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
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sll x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_dest_dep_test( 4, "sll", 0x00000001, 2, 0x00000004 ),
    gen_rr_dest_dep_test( 3, "sll", 0x00000001, 3, 0x00000008 ),
    gen_rr_dest_dep_test( 2, "sll", 0x00000001, 4, 0x00000010 ),
    gen_rr_dest_dep_test( 1, "sll", 0x00000001, 5, 0x00000020 ),
    gen_rr_dest_dep_test( 0, "sll", 0x00000001, 31, 0x80000000 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_src0_dep_test( 4, "sll", 0x00000002, 1, 0x00000004 ),
    gen_rr_src0_dep_test( 3, "sll", 0x00000004, 1, 0x00000008 ),
    gen_rr_src0_dep_test( 2, "sll", 0x00000008, 1, 0x00000010 ),
    gen_rr_src0_dep_test( 1, "sll", 0x00000010, 1, 0x00000020 ),
    gen_rr_src0_dep_test( 0, "sll", 0x00000020, 1, 0x00000040 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_src1_dep_test( 4, "sll", 0x00000001, 2, 0x00000004 ),
    gen_rr_src1_dep_test( 3, "sll", 0x00000001, 3, 0x00000008 ),
    gen_rr_src1_dep_test( 2, "sll", 0x00000001, 4, 0x00000010 ),
    gen_rr_src1_dep_test( 1, "sll", 0x00000001, 5, 0x00000020 ),
    gen_rr_src1_dep_test( 0, "sll", 0x00000001, 31, 0x80000000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_srcs_dep_test( 4, "sll", 0x00000002, 2, 0x00000008 ),
    gen_rr_srcs_dep_test( 3, "sll", 0x00000004, 3, 0x00000020 ),
    gen_rr_srcs_dep_test( 2, "sll", 0x00000008, 4, 0x00000080 ),
    gen_rr_srcs_dep_test( 1, "sll", 0x00000010, 5, 0x00000200 ),
    gen_rr_srcs_dep_test( 0, "sll", 0x00000020, 6, 0x00000800 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_src1_eq_dest_test( "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_src0_eq_src1_test( "sll", 1, 0x00000002 ),
    gen_rr_srcs_eq_dest_test( "sll", 1, 0x00000002 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sll", 0x00000001, 0, 0x00000001 ),
    gen_rr_value_test( "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_value_test( "sll", 0x00000001, 2, 0x00000004 ),
    gen_rr_value_test( "sll", 0x00000001, 4, 0x00000010 ),
    gen_rr_value_test( "sll", 0x00000001, 8, 0x00000100 ),
    gen_rr_value_test( "sll", 0x00000001, 16, 0x00010000 ),
    gen_rr_value_test( "sll", 0x00000001, 31, 0x80000000 ),

    gen_rr_value_test( "sll", 0x80000000, 1, 0x00000000 ),
    gen_rr_value_test( "sll", 0x80000000, 31, 0x00000000 ),

    gen_rr_value_test( "sll", 0xFFFFFFFF, 1, 0xFFFFFFFE ),
    gen_rr_value_test( "sll", 0xFFFFFFFF, 2, 0xFFFFFFFC ),
    gen_rr_value_test( "sll", 0xFFFFFFFF, 31, 0x80000000 ),

    gen_rr_value_test( "sll", 0x12345678, 4, 0x23456780 ),
    gen_rr_value_test( "sll", 0x12345678, 8, 0x34567800 ),
    gen_rr_value_test( "sll", 0x12345678, 16, 0x56780000 ),

    gen_rr_value_test( "sll", 0x00000001, 32, 0x00000001 ),  # Shift amount modulo 32
    gen_rr_value_test( "sll", 0x00000001, 33, 0x00000002 ),
    gen_rr_value_test( "sll", 0x00000001, 64, 0x00000001 ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = random.randint(0, 0xFFFFFFFF)
    src1 = random.randint(0, 31)
    dest = (src0 << src1) & 0xFFFFFFFF
    asm_code.append( gen_rr_value_test( "sll", src0, src1, dest ) )
  return asm_code
