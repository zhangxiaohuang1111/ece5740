#=========================================================================
# srl
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
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srl x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "srl", 0xFFFFFFFF, 1, 0x7FFFFFFF ),
    gen_rr_dest_dep_test( 4, "srl", 0xFFFFFFFF, 2, 0x3FFFFFFF ),
    gen_rr_dest_dep_test( 3, "srl", 0xFFFFFFFF, 3, 0x1FFFFFFF ),
    gen_rr_dest_dep_test( 2, "srl", 0xFFFFFFFF, 4, 0x0FFFFFFF ),
    gen_rr_dest_dep_test( 1, "srl", 0xFFFFFFFF, 5, 0x07FFFFFF ),
    gen_rr_dest_dep_test( 0, "srl", 0xFFFFFFFF, 31, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "srl", 0x80000000, 1, 0x40000000 ),
    gen_rr_src0_dep_test( 4, "srl", 0x80000000, 2, 0x20000000 ),
    gen_rr_src0_dep_test( 3, "srl", 0x80000000, 3, 0x10000000 ),
    gen_rr_src0_dep_test( 2, "srl", 0x80000000, 4, 0x08000000 ),
    gen_rr_src0_dep_test( 1, "srl", 0x80000000, 5, 0x04000000 ),
    gen_rr_src0_dep_test( 0, "srl", 0x80000000, 31, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "srl", 0x12345678, 1, 0x091A2B3C ),
    gen_rr_src1_dep_test( 4, "srl", 0x12345678, 2, 0x048D159E ),
    gen_rr_src1_dep_test( 3, "srl", 0x12345678, 3, 0x02468ACF ),
    gen_rr_src1_dep_test( 2, "srl", 0x12345678, 4, 0x01234567 ),
    gen_rr_src1_dep_test( 1, "srl", 0x12345678, 5, 0x0091A2B3 ),
    gen_rr_src1_dep_test( 0, "srl", 0x12345678, 31, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "srl", 0x00000008, 1, 0x00000004 ),
    gen_rr_srcs_dep_test( 4, "srl", 0x00000010, 2, 0x00000004 ),
    gen_rr_srcs_dep_test( 3, "srl", 0x00000020, 3, 0x00000004 ),
    gen_rr_srcs_dep_test( 2, "srl", 0x00000040, 4, 0x00000004 ),
    gen_rr_srcs_dep_test( 1, "srl", 0x00000080, 5, 0x00000004 ),
    gen_rr_srcs_dep_test( 0, "srl", 0xFFFFFFFF, 4, 0x0FFFFFFF ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "srl", 0x80000000, 1, 0x40000000 ),
    gen_rr_src1_eq_dest_test( "srl", 0x80000000, 1, 0x40000000 ),
    gen_rr_src0_eq_src1_test( "srl", 4, 0x00000000 ),
    gen_rr_srcs_eq_dest_test( "srl", 8, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "srl", 0x7FFFFFFF, 0, 0x7FFFFFFF ),
    gen_rr_value_test( "srl", 0x7FFFFFFF, 1, 0x3FFFFFFF ),
    gen_rr_value_test( "srl", 0x7FFFFFFF, 31, 0x00000000 ),

    gen_rr_value_test( "srl", 0x80000000, 0, 0x80000000 ),
    gen_rr_value_test( "srl", 0x80000000, 1, 0x40000000 ),
    gen_rr_value_test( "srl", 0x80000000, 31, 0x00000001 ),

    gen_rr_value_test( "srl", 0x00000000, 0, 0x00000000 ),
    gen_rr_value_test( "srl", 0x00000000, 1, 0x00000000 ),
    gen_rr_value_test( "srl", 0x00000000, 31, 0x00000000 ),

    gen_rr_value_test( "srl", 0x12345678, 31, 0x00000000 ),
    gen_rr_value_test( "srl", 0xFFFFFFFF, 31, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = random.randint(0, 0xFFFFFFFF)
    src1 = random.randint(0, 31)
    dest = (src0 % (1 << 32)) >> src1
    asm_code.append( gen_rr_value_test( "srl", src0, src1, dest ) )
  return asm_code