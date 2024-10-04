#=========================================================================
# sub
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
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sub x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "sub", 10, 5, 5 ),  # 10 - 5 = 5
    gen_rr_dest_dep_test( 4, "sub", 20, 8, 12 ), # 20 - 8 = 12
    gen_rr_dest_dep_test( 3, "sub", 15, 3, 12 ), # 15 - 3 = 12
    gen_rr_dest_dep_test( 2, "sub", 30, 10, 20 ),# 30 - 10 = 20
    gen_rr_dest_dep_test( 1, "sub", 50, 25, 25 ),# 50 - 25 = 25
    gen_rr_dest_dep_test( 0, "sub", 100, 50, 50 ),# 100 - 50 = 50
    gen_rr_dest_dep_test( 0, "sub", 75, 25, 50 ),# 75 - 25 = 50
    gen_rr_dest_dep_test( 0, "sub", 60, 30, 30 ),# 60 - 30 = 30
    gen_rr_dest_dep_test( 0, "sub", 40, 10, 30 ),# 40 - 10 = 30
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sub", 20,  5, 15 ),  # 20 - 5 = 15
    gen_rr_src0_dep_test( 4, "sub", 30, 10, 20 ),  # 30 - 10 = 20
    gen_rr_src0_dep_test( 3, "sub", 40, 20, 20 ),  # 40 - 20 = 20
    gen_rr_src0_dep_test( 2, "sub", 50, 25, 25 ),  # 50 - 25 = 25
    gen_rr_src0_dep_test( 1, "sub", 60, 30, 30 ),  # 60 - 30 = 30
    gen_rr_src0_dep_test( 0, "sub", 100, 50, 50 ), # 100 - 50 = 50
    gen_rr_src0_dep_test( 0, "sub", 75,  25, 50 ), # 75 - 25 = 50
    gen_rr_src0_dep_test( 0, "sub", 90,  45, 45 ), # 90 - 45 = 45
    gen_rr_src0_dep_test( 0, "sub", 80,  40, 40 ), # 80 - 40 = 40
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5,  "sub", 10, 5,  5 ),  # 10 - 5  = 5
    gen_rr_src1_dep_test( 4,  "sub", 20, 8,  12 ), # 20 - 8  = 12
    gen_rr_src1_dep_test( 3,  "sub", 30, 9,  21 ), # 30 - 9  = 21
    gen_rr_src1_dep_test( 2,  "sub", 40, 10, 30 ), # 40 - 10 = 30
    gen_rr_src1_dep_test( 1,  "sub", 50, 20, 30 ), # 50 - 20 = 30
    gen_rr_src1_dep_test( 0,  "sub", 60, 30, 30 ), # 60 - 30 = 30
    gen_rr_src1_dep_test( 6,  "sub", 70, 35, 35 ), # 70 - 35 = 35
    gen_rr_src1_dep_test( 7,  "sub", 80, 40, 40 ), # 80 - 40 = 40
    gen_rr_src1_dep_test( 8,  "sub", 90, 45, 45 ), # 90 - 45 = 45
    gen_rr_src1_dep_test( 9,  "sub", 100, 50, 50 ),# 100 - 50 = 50
    gen_rr_src1_dep_test( 10, "sub", 110, 55, 55 ),# 110 - 55 = 55
    gen_rr_src1_dep_test( 11, "sub", 120, 60, 60 ),# 120 - 60 = 60
    gen_rr_src1_dep_test( 12, "sub", 130, 65, 65 ),# 130 - 65 = 65
    gen_rr_src1_dep_test( 13, "sub", 140, 70, 70 ),# 140 - 70 = 70
    gen_rr_src1_dep_test( 14, "sub", 150, 75, 75 ),# 150 - 75 = 75
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sub", 12, 2, 10 ),  # 12 - 2 = 10
    gen_rr_srcs_dep_test( 4, "sub", 13, 3, 10 ),  # 13 - 3 = 10
    gen_rr_srcs_dep_test( 3, "sub", 14, 4, 10 ),  # 14 - 4 = 10
    gen_rr_srcs_dep_test( 2, "sub", 15, 5, 10 ),  # 15 - 5 = 10
    gen_rr_srcs_dep_test( 1, "sub", 16, 6, 10 ),  # 16 - 6 = 10
    gen_rr_srcs_dep_test( 0, "sub", 17, 7, 10 ),  # 17 - 7 = 10
    gen_rr_srcs_dep_test( 0, "sub", 20, 10, 10 ), # 20 - 10 = 10
    gen_rr_srcs_dep_test( 0, "sub", 25, 5, 20 ),  # 25 - 5 = 20
    gen_rr_srcs_dep_test( 0, "sub", 30, 0, 30 ),  # 30 - 0 = 30
    gen_rr_srcs_dep_test( 0, "sub", 40, 20, 20 ), # 40 - 20 = 20
    gen_rr_srcs_dep_test( 0, "sub", 50, 25, 25 ), # 50 - 25 = 25
    gen_rr_srcs_dep_test( 0, "sub", 100, 50, 50 ),# 100 - 50 = 50
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sub", 25, 1, 24 ),   # 25 - 1 = 24 (src0 == dest)
    gen_rr_src1_eq_dest_test( "sub", 26, 1, 25 ),   # 26 - 1 = 25 (src1 == dest)
    gen_rr_src0_eq_src1_test( "sub", 27, 0 ),       # 27 - 27 = 0 (src0 == src1)
    gen_rr_srcs_eq_dest_test( "sub", 28, 0 ),       # 28 - 28 = 0 (src0 == src1 == dest)
    gen_rr_src0_eq_dest_test( "sub", 22, 2, 20 ),   # 22 - 2 = 20 (src0 == dest)
    gen_rr_src1_eq_dest_test( "sub", 1, 1, 0 ),     # 1 - 1 = 0 (src1 == dest)
    gen_rr_src0_eq_src1_test( "sub", 30, 0 ),       # 30 - 30 = 0 (src0 == src1)
    gen_rr_srcs_eq_dest_test( "sub", 50, 0 ),       # 50 - 50 = 0 (src0 == src1 == dest)
    gen_rr_src0_eq_dest_test( "sub", 100, 1, 99 ),  # 100 - 1 = 99 (src0 == dest)
    gen_rr_src1_eq_dest_test( "sub", 200, 1, 199 ), # 200 - 1 = 199 (src1 == dest)
    gen_rr_src0_eq_src1_test( "sub", 100, 0 ),      # 100 - 100 = 0 (src0 == src1)
    gen_rr_srcs_eq_dest_test( "sub", 200, 0 ),      # 200 - 200 = 0 (src0 == src1 == dest)
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "sub", 0x00000000, 0x00000000, 0x00000000 ), 
    gen_rr_value_test( "sub", 0x00000001, 0x00000001, 0x00000000 ), 
    gen_rr_value_test( "sub", 0x00000007, 0x00000003, 0x00000004 ), 
    gen_rr_value_test( "sub", 0x00000000, 0xffff8000, 0x00008000 ), 
    gen_rr_value_test( "sub", 0x80000000, 0x00000000, 0x80000000 ), 
    gen_rr_value_test( "sub", 0x80000000, 0xffff8000, 0x80008000 ),
    gen_rr_value_test( "sub", 0x00000000, 0x00007fff, 0xffff8001 ), 
    gen_rr_value_test( "sub", 0x7fffffff, 0x00000000, 0x7fffffff ),
    gen_rr_value_test( "sub", 0x7fffffff, 0x00007fff, 0x7fff8000 ), 
    gen_rr_value_test( "sub", 0x80000000, 0x00007fff, 0x7fff8001 ), 
    gen_rr_value_test( "sub", 0x7fffffff, 0xffff8000, 0x80007fff ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0xffffffff) )
    dest = src0 - src1
    asm_code.append( gen_rr_value_test( "sub", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
