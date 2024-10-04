#=========================================================================
# sltu
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
    csrr x1, mngr2proc < 4
    csrr x2, mngr2proc < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sltu x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "sltu", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_dest_dep_test( 4, "sltu", 0x00000003, 0x00000003, 0x00000000 ),
    gen_rr_dest_dep_test( 3, "sltu", 0x00000004, 0x00000002, 0x00000000 ),
    gen_rr_dest_dep_test( 2, "sltu", 0xFFFFFFFF, 0x00000000, 0x00000000 ),  # Max unsigned > 0
    gen_rr_dest_dep_test( 1, "sltu", 0x00000000, 0xFFFFFFFF, 0x00000001 ),  # 0 < Max unsigned
    gen_rr_dest_dep_test( 0, "sltu", 0x80000000, 0x7FFFFFFF, 0x00000000 ),  # Larger unsigned value
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sltu", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_src0_dep_test( 4, "sltu", 0x00000002, 0x00000002, 0x00000000 ),
    gen_rr_src0_dep_test( 3, "sltu", 0x00000003, 0x00000002, 0x00000000 ),
    gen_rr_src0_dep_test( 2, "sltu", 0xFFFFFFFF, 0x00000000, 0x00000000 ),  # Max unsigned > 0
    gen_rr_src0_dep_test( 1, "sltu", 0x00000000, 0xFFFFFFFF, 0x00000001 ),  # 0 < Max unsigned
    gen_rr_src0_dep_test( 0, "sltu", 0x7FFFFFFF, 0x80000000, 0x00000001 ),  # Smaller unsigned value
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sltu", 0x00000002, 0x00000003, 0x00000001 ),
    gen_rr_src1_dep_test( 4, "sltu", 0x00000002, 0x00000002, 0x00000000 ),
    gen_rr_src1_dep_test( 3, "sltu", 0x00000002, 0x00000001, 0x00000000 ),
    gen_rr_src1_dep_test( 2, "sltu", 0x00000000, 0xFFFFFFFF, 0x00000001 ),  # 0 < Max unsigned
    gen_rr_src1_dep_test( 1, "sltu", 0xFFFFFFFF, 0x00000000, 0x00000000 ),  # Max unsigned > 0
    gen_rr_src1_dep_test( 0, "sltu", 0x80000000, 0x7FFFFFFF, 0x00000000 ),  # Larger unsigned value
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sltu", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_srcs_dep_test( 4, "sltu", 0x00000002, 0x00000002, 0x00000000 ),
    gen_rr_srcs_dep_test( 3, "sltu", 0x00000003, 0x00000002, 0x00000000 ),
    gen_rr_srcs_dep_test( 2, "sltu", 0xFFFFFFFF, 0xFFFFFFFE, 0x00000000 ),  # Max unsigned > one less
    gen_rr_srcs_dep_test( 1, "sltu", 0x00000000, 0x00000001, 0x00000001 ),  # 0 < 1
    gen_rr_srcs_dep_test( 0, "sltu", 0x7FFFFFFF, 0x80000000, 0x00000001 ),  # Smaller unsigned value
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sltu", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_src1_eq_dest_test( "sltu", 0x00000002, 0x00000001, 0x00000000 ),
    gen_rr_src0_eq_src1_test( "sltu", 0x00000003, 0x00000000 ),  # Equal values
    gen_rr_srcs_eq_dest_test( "sltu", 0x00000004, 0x00000000 ),  # Equal values
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    # Test with small unsigned values
    gen_rr_value_test( "sltu", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_value_test( "sltu", 0x00000002, 0x00000001, 0x00000000 ),
    gen_rr_value_test( "sltu", 0x00000000, 0x00000000, 0x00000000 ),

    # Test with large unsigned values
    gen_rr_value_test( "sltu", 0xFFFFFFFF, 0x00000000, 0x00000000 ),  # Max unsigned > 0
    gen_rr_value_test( "sltu", 0x00000000, 0xFFFFFFFF, 0x00000001 ),  # 0 < Max unsigned
    gen_rr_value_test( "sltu", 0x80000000, 0x7FFFFFFF, 0x00000000 ),  # Larger unsigned value

    # Test boundary conditions
    gen_rr_value_test( "sltu", 0xFFFFFFFF, 0xFFFFFFFF, 0x00000000 ),  # Equal max unsigned
    gen_rr_value_test( "sltu", 0x7FFFFFFF, 0x7FFFFFFF, 0x00000000 ),  # Equal mid-range values
    gen_rr_value_test( "sltu", 0x00000000, 0x00000001, 0x00000001 ),  # Min unsigned < 1
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0xffffffff) )
    dest = b32( src0.uint() < src1.uint() )
    asm_code.append( gen_rr_value_test( "sltu", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
