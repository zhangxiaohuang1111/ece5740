#=========================================================================
# mul
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
    mul x3, x1, x2
    mul x3 ,x3, x1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 100
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
    gen_rr_dest_dep_test( 50, "mul", 1, 1, 1 ),
    gen_rr_dest_dep_test( 4,  "mul", 1, 1, 1 ),
    gen_rr_dest_dep_test( 3,  "mul", 1, 1, 1 ),
    gen_rr_dest_dep_test( 2,  "mul", 1, 1, 1 ),
    gen_rr_dest_dep_test( 1,  "mul", 100, 1, 100 ),
    gen_rr_dest_dep_test( 0,  "mul", 1, 1, 1 ),
    gen_rr_dest_dep_test( 4,  "mul", 2, 1, 2 ),
    gen_rr_dest_dep_test( 3,  "mul", 3, 1, 3 ),
    gen_rr_dest_dep_test( 2,  "mul", 4, 1, 4 ),
    gen_rr_dest_dep_test( 1,  "mul", 5, 1, 5 ),
    gen_rr_dest_dep_test( 0,  "mul", 6, 1, 6 ),
    gen_rr_dest_dep_test( 0,  "mul", 20, 1, 20 ),
    gen_rr_dest_dep_test( 0,  "mul", 15, 1, 15 ),
    gen_rr_dest_dep_test( 0,  "mul", 25, 1, 25 ),
    gen_rr_dest_dep_test( 0,  "mul", 0, 1, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5,  "mul",  7, 1,  7 ),
    gen_rr_src0_dep_test( 4,  "mul",  8, 1,  8 ),
    gen_rr_src0_dep_test( 3,  "mul",  9, 1,  9 ),
    gen_rr_src0_dep_test( 2,  "mul", 10, 1, 10 ),
    gen_rr_src0_dep_test( 1,  "mul", 11, 1, 11 ),
    gen_rr_src0_dep_test( 0,  "mul", 12, 1, 12 ),
    gen_rr_src0_dep_test( 6,  "mul", 13, 1, 13 ),
    gen_rr_src0_dep_test( 7,  "mul", 14, 1, 14 ),
    gen_rr_src0_dep_test( 8,  "mul", 15, 1, 15 ),
    gen_rr_src0_dep_test( 9,  "mul", 16, 1, 16 ),
    gen_rr_src0_dep_test( 10, "mul", 17, 1, 17 ),
    gen_rr_src0_dep_test( 11, "mul", 18, 1, 18 ),
    gen_rr_src0_dep_test( 12, "mul", 19, 1, 19 ),
    gen_rr_src0_dep_test( 13, "mul", 20, 1, 20 ),
    gen_rr_src0_dep_test( 14, "mul", 21, 1, 21 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5,  "mul", 1, 13, 13 ),
    gen_rr_src1_dep_test( 4,  "mul", 1, 14, 14 ),
    gen_rr_src1_dep_test( 3,  "mul", 1, 15, 15 ),
    gen_rr_src1_dep_test( 2,  "mul", 1, 16, 16 ),
    gen_rr_src1_dep_test( 1,  "mul", 1, 17, 17 ),
    gen_rr_src1_dep_test( 0,  "mul", 1, 18, 18 ),
    gen_rr_src1_dep_test( 6,  "mul", 1, 19, 19 ),
    gen_rr_src1_dep_test( 7,  "mul", 1, 20, 20 ),
    gen_rr_src1_dep_test( 8,  "mul", 1, 21, 21 ),
    gen_rr_src1_dep_test( 9,  "mul", 1, 22, 22 ),
    gen_rr_src1_dep_test( 10, "mul", 1, 23, 23 ),
    gen_rr_src1_dep_test( 11, "mul", 1, 24, 24 ),
    gen_rr_src1_dep_test( 12, "mul", 1, 25, 25 ),
    gen_rr_src1_dep_test( 13, "mul", 1, 26, 26 ),
    gen_rr_src1_dep_test( 14, "mul", 1, 27, 27 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "mul", 12, 2, 24 ),  # 12 * 2 = 24
    gen_rr_srcs_dep_test( 4, "mul", 13, 3, 39 ),  # 13 * 3 = 39
    gen_rr_srcs_dep_test( 3, "mul", 14, 4, 56 ),  # 14 * 4 = 56
    gen_rr_srcs_dep_test( 2, "mul", 15, 5, 75 ),  # 15 * 5 = 75
    gen_rr_srcs_dep_test( 1, "mul", 16, 6, 96 ),  # 16 * 6 = 96
    gen_rr_srcs_dep_test( 0, "mul", 17, 7, 119 ), # 17 * 7 = 119
    gen_rr_srcs_dep_test( 0, "mul", 18, 8, 144 ), # 18 * 8 = 144
    gen_rr_srcs_dep_test( 0, "mul", 19, 9, 171 ), # 19 * 9 = 171
    gen_rr_srcs_dep_test( 0, "mul", 20, 10, 200 ),# 20 * 10 = 200
    gen_rr_srcs_dep_test( 0, "mul", 21, 11, 231 ),# 21 * 11 = 231
    gen_rr_srcs_dep_test( 0, "mul", 22, 12, 264 ),# 22 * 12 = 264
    gen_rr_srcs_dep_test( 0, "mul", 23, 13, 299 ),# 23 * 13 = 299
    gen_rr_srcs_dep_test( 0, "mul", 24, 14, 336 ),# 24 * 14 = 336
    gen_rr_srcs_dep_test( 0, "mul", 25, 15, 375 ),# 25 * 15 = 375
    gen_rr_srcs_dep_test( 0, "mul", 26, 16, 416 ),# 26 * 16 = 416
    gen_rr_srcs_dep_test( 0, "mul", 27, 17, 459 ),# 27 * 17 = 459
    gen_rr_srcs_dep_test( 0, "mul", 28, 18, 504 ),# 28 * 18 = 504
    gen_rr_srcs_dep_test( 0, "mul", 29, 19, 551 ),# 29 * 19 = 551
    gen_rr_srcs_dep_test( 0, "mul", 30, 20, 600 ),# 30 * 20 = 600
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "mul", 25, 1, 25 ),
    gen_rr_src0_eq_dest_test( "mul", 22, 1, 22 ),
    gen_rr_src0_eq_dest_test( "mul", 100, 1, 100 ),
    gen_rr_src1_eq_dest_test( "mul", 26, 1, 26 ),
    gen_rr_src1_eq_dest_test( "mul", 1, 1, 1 ),
    gen_rr_src1_eq_dest_test( "mul", 200, 1, 200 ),
    gen_rr_srcs_eq_dest_test( "mul", 28, 784 ),
    gen_rr_srcs_eq_dest_test( "mul", 50, 2500 ),
    gen_rr_srcs_eq_dest_test( "mul", 200, 40000 ),
    gen_rr_src0_eq_src1_test( "mul", 100, 10000 ),
    gen_rr_src0_eq_src1_test( "mul", 27, 729 ),
    gen_rr_src0_eq_src1_test( "mul", 30, 900 ),

  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "mul", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "mul", 0x00000001, 0x00000001, 0x00000001 ),
    gen_rr_value_test( "mul", 0x00000003, 0x00000007, 0x00000015 ),
    gen_rr_value_test( "mul", 0x00000000, 0xffff8000, 0x00000000 ),
    gen_rr_value_test( "mul", 0x80000000, 0x00000001, 0x80000000 ),
    gen_rr_value_test( "mul", 0x80000000, 0xffff8000, 0x00000000 ),
    gen_rr_value_test( "mul", 0x00000000, 0x00007fff, 0x00000000 ),
    gen_rr_value_test( "mul", 0x7fffffff, 0x00000001, 0x7fffffff ),
    gen_rr_value_test( "mul", 0x7fffffff, 0x00007fff, 0x7fff8001 ),
    gen_rr_value_test( "mul", 0x80000000, 0x00007fff, 0x80000000 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0xffffffff) )
    dest = src0 * src1
    asm_code.append( gen_rr_value_test( "mul", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code