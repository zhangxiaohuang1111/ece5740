#=========================================================================
# bge
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

    # Use x3 to track the control flow pattern
    addi  x3, x0, 0

    csrr  x1, mngr2proc < 2
    csrr  x2, mngr2proc < 2

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    bge   x1, x2, label_a
    addi  x3, x3, 0b01

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

  label_a:
    addi  x3, x3, 0b10

    # Only the second bit should be set if branch was taken
    csrw proc2mngr, x3 > 0b10

  """

#-------------------------------------------------------------------------
# gen_src0_dep_taken_test
#-------------------------------------------------------------------------

# Test where src0 > src1 (branch should be taken)
def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "bge", 10, 1, True ),  # 10 > 1, branch taken
    gen_br2_src0_dep_test( 4, "bge", 9, 2, True ),   # 9 > 2, branch taken
    gen_br2_src0_dep_test( 3, "bge", 8, 3, True ),   # 8 > 3, branch taken
    gen_br2_src0_dep_test( 2, "bge", 7, 4, True ),   # 7 > 4, branch taken
    gen_br2_src0_dep_test( 1, "bge", 6, 5, True ),   # 6 > 5, branch taken
    gen_br2_src0_dep_test( 0, "bge", 100, -100, True ),  # 100 > -100, branch taken
  ]
#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

# Test where src0 < src1 (branch should not be taken)
def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bge", 1, 10, False ),  # 1 < 10, branch not taken
    gen_br2_src0_dep_test( 4, "bge", 2, 9, False ),   # 2 < 9, branch not taken
    gen_br2_src0_dep_test( 3, "bge", 3, 8, False ),   # 3 < 8, branch not taken
    gen_br2_src0_dep_test( 2, "bge", 4, 7, False ),   # 4 < 7, branch not taken
    gen_br2_src0_dep_test( 1, "bge", 5, 6, False ),   # 5 < 6, branch not taken
    gen_br2_src0_dep_test( 0, "bge", -100, 100, False ),  # -100 < 100, branch not taken
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

# Test where src0 > src1 (branch should be taken)
def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bge", 7, 1, True ),  # 7 > 1, branch taken
    gen_br2_src1_dep_test( 4, "bge", 7, 2, True ),  # 7 > 2, branch taken
    gen_br2_src1_dep_test( 3, "bge", 7, 3, True ),  # 7 > 3, branch taken
    gen_br2_src1_dep_test( 2, "bge", 7, 4, True ),  # 7 > 4, branch taken
    gen_br2_src1_dep_test( 1, "bge", 7, 5, True ),  # 7 > 5, branch taken
    gen_br2_src1_dep_test( 0, "bge", 7, 6, True ),  # 7 > 6, branch taken
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

# Test where src0 < src1 (branch should not be taken)
def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bge", 1, 7, False ),  # 1 < 7, branch not taken
    gen_br2_src1_dep_test( 4, "bge", 2, 7, False ),  # 2 < 7, branch not taken
    gen_br2_src1_dep_test( 3, "bge", 3, 7, False ),  # 3 < 7, branch not taken
    gen_br2_src1_dep_test( 2, "bge", 4, 7, False ),  # 4 < 7, branch not taken
    gen_br2_src1_dep_test( 1, "bge", 5, 7, False ),  # 5 < 7, branch not taken
    gen_br2_src1_dep_test( 0, "bge", 6, 7, False ),  # 6 < 7, branch not taken
  ]
#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

# Test where src0 > src1 (branch should be taken)
def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bge", 2, 1, True ),  # 2 > 1, branch taken
    gen_br2_srcs_dep_test( 4, "bge", 3, 2, True ),  # 3 > 2, branch taken
    gen_br2_srcs_dep_test( 3, "bge", 4, 3, True ),  # 4 > 3, branch taken
    gen_br2_srcs_dep_test( 2, "bge", 5, 4, True ),  # 5 > 4, branch taken
    gen_br2_srcs_dep_test( 1, "bge", 6, 5, True ),  # 6 > 5, branch taken
    gen_br2_srcs_dep_test( 0, "bge", 7, 6, True ),  # 7 > 6, branch taken
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

# Test where src0 < src1 (branch should not be taken)
def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bge", 1, 2, False ),  # 1 < 2, branch not taken
    gen_br2_srcs_dep_test( 4, "bge", 2, 3, False ),  # 2 < 3, branch not taken
    gen_br2_srcs_dep_test( 3, "bge", 3, 4, False ),  # 3 < 4, branch not taken
    gen_br2_srcs_dep_test( 2, "bge", 4, 5, False ),  # 4 < 5, branch not taken
    gen_br2_srcs_dep_test( 1, "bge", 5, 6, False ),  # 5 < 6, branch not taken
    gen_br2_srcs_dep_test( 0, "bge", 6, 7, False ),  # 6 < 7, branch not taken
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_test
#-------------------------------------------------------------------------

# Test where src0 == src1 (branch should be taken)
def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bge", 1, True ),  # 1 == 1, branch taken
    gen_br2_src0_eq_src1_test( "bge", 0, True ),  # 0 == 0, branch taken
    gen_br2_src0_eq_src1_test( "bge", -1, True ),  # -1 == -1, branch taken
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "bge", -1, -1, True ),
    gen_br2_value_test( "bge", -1,  0, False ),
    gen_br2_value_test( "bge", -1,  1, False ),

    gen_br2_value_test( "bge",  0, -1, True ),
    gen_br2_value_test( "bge",  0,  0, True ),
    gen_br2_value_test( "bge",  0,  1, False ),

    gen_br2_value_test( "bge",  1, -1, True ),
    gen_br2_value_test( "bge",  1,  0, True ),
    gen_br2_value_test( "bge",  1,  1, True ),

    gen_br2_value_test( "bge", 0xfffffff7, 0xfffffff7, True ),
    gen_br2_value_test( "bge", 0x7fffffff, 0x7fffffff, True ),
    gen_br2_value_test( "bge", 0xfffffff7, 0x7fffffff, False ),
    gen_br2_value_test( "bge", 0x7fffffff, 0xfffffff7, True ),

    # src0 == src1 (branch taken)
    gen_br2_value_test( "bge", -1, -1, True ),  # -1 == -1, branch taken
    gen_br2_value_test( "bge",  0,  0, True ),  # 0 == 0, branch taken
    gen_br2_value_test( "bge",  1,  1, True ),  # 1 == 1, branch taken

    # src0 > src1 (branch taken)
    gen_br2_value_test( "bge",  0, -1, True ),  # 0 > -1, branch taken
    gen_br2_value_test( "bge",  1,  0, True ),  # 1 > 0, branch taken
    gen_br2_value_test( "bge", 0x7fffffff, 0x7fffffff, True ),  # max == max, branch taken

    # src0 < src1 (branch not taken)
    gen_br2_value_test( "bge", -1,  0, False ),  # -1 < 0, branch not taken
    gen_br2_value_test( "bge", -1,  1, False ),  # -1 < 1, branch not taken
    gen_br2_value_test( "bge", 0xfffffff7, 0x7fffffff, False ),  # large negative < positive, branch not taken

    # Mixed positive and negative values
    gen_br2_value_test( "bge", 0x7fffffff, -1, True ),  # max positive > -1, branch taken
    gen_br2_value_test( "bge", -1, 0x7fffffff, False ),  # -1 < max positive, branch not taken
  ]
  

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

# Random test cases with bge, covering both greater, equal, and less scenarios
def gen_random_test():
  asm_code = []
  for i in range(25):
    taken = random.choice([True, False])
    src0  = random.randint(-2147483648, 2147483647)  # Generate a signed 32-bit integer

    if taken:
      # Branch taken, src0 >= src1 (includes both "greater" and "equal" cases)
      if random.choice([True, False]):  # Randomly decide between equal or greater case
        src1 = src0  # Equal case
      else:
        src1 = random.randint(-2147483648, src0)  # Greater case
    else:
      # Branch not taken, src0 < src1
      src1 = random.randint(src0 + 1, 2147483647)  # Smaller case

    # Append the test case to asm_code
    asm_code.append( gen_br2_value_test( "bge", src0, src1, taken ) )
  
  return asm_code

#-------------------------------------------------------------------------
# gen_back_to_back_test
#-------------------------------------------------------------------------

# Test multiple consecutive bge instructions
def gen_back_to_back_test():
  return """
     # Test backwards walk (back to back branch taken)

     csrr x3, mngr2proc < 1
     csrr x1, mngr2proc < 1

     bge  x3, x0, X0
     csrw proc2mngr, x0
     nop
     a0:
     csrw proc2mngr, x1 > 1
     bge  x3, x0, y0
     b0:
     bge  x3, x0, a0
     c0:
     bge  x3, x0, b0
     d0:
     bge  x3, x0, c0
     e0:
     bge  x3, x0, d0
     f0:
     bge  x3, x0, e0
     g0:
     bge  x3, x0, f0
     h0:
     bge  x3, x0, g0
     i0:
     bge  x3, x0, h0
     X0:
     bge  x3, x0, i0
     y0:

     bge  x3, x0, X1
     csrw proc2mngr, x0
     nop
     a1:
     csrw proc2mngr, x1 > 1
     bge  x3, x0, y1
     b1:
     bge  x3, x0, a1
     c1:
     bge  x3, x0, b1
     d1:
     bge  x3, x0, c1
     e1:
     bge  x3, x0, d1
     f1:
     bge  x3, x0, e1
     g1:
     bge  x3, x0, f1
     h1:
     bge  x3, x0, g1
     i1:
     bge  x3, x0, h1
     X1:
     bge  x3, x0, i1
     y1:
     nop
     nop
     nop
     nop
     nop
     nop
     nop
  """