#=========================================================================
# slt
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
    slt x3, x1, x2
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

#=========================================================================
# slt
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
    csrr x1, mngr2proc < 0x00000005   # Load x1 with 5
    csrr x2, mngr2proc < 0x00000007   # Load x2 with 7
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slt x3, x1, x2                    # x3 = (x1 < x2) ? 1 : 0
    slt x4, x2, x1                    # x4 = (x2 < x1) ? 1 : 0
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00000001   # Expect x3 to be 1
    csrw proc2mngr, x4 > 0x00000000   # Expect x4 to be 0
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
    gen_rr_dest_dep_test( 5, "slt", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_dest_dep_test( 4, "slt", 0x00000003, 0x00000003, 0x00000000 ),
    gen_rr_dest_dep_test( 3, "slt", 0x00000004, 0x00000002, 0x00000000 ),
    gen_rr_dest_dep_test( 2, "slt", 0xFFFFFFFE, 0xFFFFFFFF, 0x00000001 ),  # Negative numbers
    gen_rr_dest_dep_test( 1, "slt", 0x80000000, 0x00000000, 0x00000001 ),  # Negative vs positive
    gen_rr_dest_dep_test( 0, "slt", 0x7FFFFFFF, 0x80000000, 0x00000000 ),  # Positive vs negative
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "slt", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_src0_dep_test( 4, "slt", 0x00000002, 0x00000002, 0x00000000 ),
    gen_rr_src0_dep_test( 3, "slt", 0x00000003, 0x00000002, 0x00000000 ),
    gen_rr_src0_dep_test( 2, "slt", 0xFFFFFFFF, 0x00000000, 0x00000001 ),  # -1 < 0
    gen_rr_src0_dep_test( 1, "slt", 0x00000000, 0xFFFFFFFF, 0x00000000 ),  # 0 < -1
    gen_rr_src0_dep_test( 0, "slt", 0x80000000, 0x7FFFFFFF, 0x00000001 ),  # Smallest negative < largest positive
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "slt", 0x00000002, 0x00000003, 0x00000001 ),
    gen_rr_src1_dep_test( 4, "slt", 0x00000002, 0x00000002, 0x00000000 ),
    gen_rr_src1_dep_test( 3, "slt", 0x00000002, 0x00000001, 0x00000000 ),
    gen_rr_src1_dep_test( 2, "slt", 0x00000000, 0xFFFFFFFF, 0x00000000 ),  # 0 < -1
    gen_rr_src1_dep_test( 1, "slt", 0xFFFFFFFF, 0x00000000, 0x00000001 ),  # -1 < 0
    gen_rr_src1_dep_test( 0, "slt", 0x7FFFFFFF, 0x80000000, 0x00000000 ),  # Largest positive < smallest negative
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "slt", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_srcs_dep_test( 4, "slt", 0x00000002, 0x00000002, 0x00000000 ),
    gen_rr_srcs_dep_test( 3, "slt", 0x00000003, 0x00000002, 0x00000000 ),
    gen_rr_srcs_dep_test( 2, "slt", 0x80000000, 0x00000000, 0x00000001 ),  # Negative vs positive
    gen_rr_srcs_dep_test( 1, "slt", 0x7FFFFFFF, 0xFFFFFFFF, 0x00000000 ),  # Positive vs negative
    gen_rr_srcs_dep_test( 0, "slt", 0xFFFFFFFF, 0x7FFFFFFF, 0x00000001 ),  # Negative vs positive
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "slt", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_src1_eq_dest_test( "slt", 0x00000002, 0x00000001, 0x00000000 ),
    gen_rr_src0_eq_src1_test( "slt", 0x00000003, 0x00000000 ),
    gen_rr_srcs_eq_dest_test( "slt", 0x00000004, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    # Test positive numbers
    gen_rr_value_test( "slt", 0x00000001, 0x00000002, 0x00000001 ),
    gen_rr_value_test( "slt", 0x00000002, 0x00000001, 0x00000000 ),
    gen_rr_value_test( "slt", 0x00000003, 0x00000003, 0x00000000 ),

    # Test negative numbers
    gen_rr_value_test( "slt", 0xFFFFFFFF, 0x00000000, 0x00000001 ),  # -1 < 0
    gen_rr_value_test( "slt", 0x80000000, 0x7FFFFFFF, 0x00000001 ),  # Smallest negative < largest positive
    gen_rr_value_test( "slt", 0x7FFFFFFF, 0x80000000, 0x00000000 ),  # Largest positive < smallest negative

    # Test mixed cases
    gen_rr_value_test( "slt", 0x00000000, 0xFFFFFFFF, 0x00000000 ),  # 0 < -1
    gen_rr_value_test( "slt", 0xFFFFFFFF, 0xFFFFFFFF, 0x00000000 ),  # -1 < -1

    # Test boundary conditions
    gen_rr_value_test( "slt", 0x7FFFFFFF, 0x7FFFFFFF, 0x00000000 ),
    gen_rr_value_test( "slt", 0x80000000, 0x80000000, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = random.randint(-2**31, 2**31 - 1)
    src1 = random.randint(-2**31, 2**31 - 1)
    dest = 1 if src0 < src1 else 0
    asm_code.append( gen_rr_value_test( "slt", src0 & 0xFFFFFFFF, src1 & 0xFFFFFFFF, dest ) )
  return asm_code
