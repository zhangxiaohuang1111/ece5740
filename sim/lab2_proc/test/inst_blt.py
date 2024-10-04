#=========================================================================
# blt
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
    csrr  x2, mngr2proc < 1

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    blt   x2, x1, label_a
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

# Test where src0 < src1 (branch should be taken)
def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "blt", 1, 10, True ),  # 1 < 10, branch taken
    gen_br2_src0_dep_test( 4, "blt", 2, 9, True ),   # 2 < 9, branch taken
    gen_br2_src0_dep_test( 3, "blt", 3, 8, True ),   # 3 < 8, branch taken
    gen_br2_src0_dep_test( 2, "blt", 4, 7, True ),   # 4 < 7, branch taken
    gen_br2_src0_dep_test( 1, "blt", 5, 6, True ),   # 5 < 6, branch taken
    gen_br2_src0_dep_test( 0, "blt", -100, 100, True ),  # -100 < 100, branch taken
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------
# Test where src0 >= src1 (branch should not be taken)
def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "blt", 10, 1, False ),  # 10 >= 1, branch not taken
    gen_br2_src0_dep_test( 4, "blt", 9, 2, False ),   # 9 >= 2, branch not taken
    gen_br2_src0_dep_test( 3, "blt", 8, 3, False ),   # 8 >= 3, branch not taken
    gen_br2_src0_dep_test( 2, "blt", 7, 4, False ),   # 7 >= 4, branch not taken
    gen_br2_src0_dep_test( 1, "blt", 6, 5, False ),   # 6 >= 5, branch not taken
    gen_br2_src0_dep_test( 0, "blt", 100, -100, False ),  # 100 >= -100, branch not taken
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------
# Test where src0 < src1 (branch should be taken)
def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "blt", 1, 7, True ),  # 1 < 7, branch taken
    gen_br2_src1_dep_test( 4, "blt", 2, 7, True ),  # 2 < 7, branch taken
    gen_br2_src1_dep_test( 3, "blt", 3, 7, True ),  # 3 < 7, branch taken
    gen_br2_src1_dep_test( 2, "blt", 4, 7, True ),  # 4 < 7, branch taken
    gen_br2_src1_dep_test( 1, "blt", 5, 7, True ),  # 5 < 7, branch taken
    gen_br2_src1_dep_test( 0, "blt", 6, 7, True ),  # 6 < 7, branch taken
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------
# Test where src0 >= src1 (branch should not be taken)
def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "blt", 7, 1, False ),  # 7 >= 1, branch not taken
    gen_br2_src1_dep_test( 4, "blt", 7, 2, False ),  # 7 >= 2, branch not taken
    gen_br2_src1_dep_test( 3, "blt", 7, 3, False ),  # 7 >= 3, branch not taken
    gen_br2_src1_dep_test( 2, "blt", 7, 4, False ),  # 7 >= 4, branch not taken
    gen_br2_src1_dep_test( 1, "blt", 7, 5, False ),  # 7 >= 5, branch not taken
    gen_br2_src1_dep_test( 0, "blt", 7, 6, False ),  # 7 >= 6, branch not taken
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------
# Test where src0 < src1 (branch should be taken)
def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "blt", 1, 2, True ),  # 1 < 2, branch taken
    gen_br2_srcs_dep_test( 4, "blt", 2, 3, True ),  # 2 < 3, branch taken
    gen_br2_srcs_dep_test( 3, "blt", 3, 4, True ),  # 3 < 4, branch taken
    gen_br2_srcs_dep_test( 2, "blt", 4, 5, True ),  # 4 < 5, branch taken
    gen_br2_srcs_dep_test( 1, "blt", 5, 6, True ),  # 5 < 6, branch taken
    gen_br2_srcs_dep_test( 0, "blt", 6, 7, True ),  # 6 < 7, branch taken
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------
# Test where src0 >= src1 (branch should not be taken)
def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "blt", 2, 1, False ),  # 2 >= 1, branch not taken
    gen_br2_srcs_dep_test( 4, "blt", 3, 2, False ),  # 3 >= 2, branch not taken
    gen_br2_srcs_dep_test( 3, "blt", 4, 3, False ),  # 4 >= 3, branch not taken
    gen_br2_srcs_dep_test( 2, "blt", 5, 4, False ),  # 5 >= 4, branch not taken
    gen_br2_srcs_dep_test( 1, "blt", 6, 5, False ),  # 6 >= 5, branch not taken
    gen_br2_srcs_dep_test( 0, "blt", 7, 6, False ),  # 7 >= 6, branch not taken
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_test
#-------------------------------------------------------------------------
# Test where src0 == src1 (branch should not be taken)
def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "blt", 1, False ),  # 1 == 1, branch not taken
    gen_br2_src0_eq_src1_test( "blt", 0, False ),  # 0 == 0, branch not taken
    gen_br2_src0_eq_src1_test( "blt", -1, False ),  # -1 == -1, branch not taken
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------
# Test various edge case values for blt (signed comparison)
def gen_value_test():
  return [

    # src0 < src1 (branch taken)
    gen_br2_value_test( "blt", -1, 0, True ),      # -1 < 0, branch taken
    gen_br2_value_test( "blt", -1, 1, True ),      # -1 < 1, branch taken
    gen_br2_value_test( "blt",  0, 1, True ),      # 0 < 1, branch taken
    gen_br2_value_test( "blt", -2147483648, 0, True ),  # Smallest signed int (-2147483648) < 0, branch taken

    # src0 == src1 (branch not taken)
    gen_br2_value_test( "blt", -1, -1, False ),    # -1 == -1, branch not taken
    gen_br2_value_test( "blt",  0,  0, False ),    # 0 == 0, branch not taken
    gen_br2_value_test( "blt",  1,  1, False ),    # 1 == 1, branch not taken
    gen_br2_value_test( "blt", 0x7fffffff, 0x7fffffff, False ),  # max positive == max positive, branch not taken

    # src0 > src1 (branch not taken)
    gen_br2_value_test( "blt",  0, -1, False ),    # 0 > -1, branch not taken
    gen_br2_value_test( "blt",  1,  0, False ),    # 1 > 0, branch not taken
    gen_br2_value_test( "blt", 0x7fffffff, 0x00000000, False ),  # max positive > 0, branch not taken
    gen_br2_value_test( "blt", 0x7fffffff, -1, False ),  # max positive > -1, branch not taken
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------


# Random test cases with blt, covering both less, equal, and greater scenarios
def gen_random_test():
  asm_code = []
  for i in range(25):
    taken = random.choice([True, False])
    src0  = random.randint(-2147483648, 2147483647)  # Generate a signed 32-bit integer

    if taken:
      # Branch taken, src0 < src1
      src1 = random.randint(src0 + 1, 2147483647)  # Ensure src1 > src0 (small case)
    else:
      # Branch not taken, src0 >= src1
      src1 = random.randint(-2147483648, src0)  # Ensure src0 >= src1 (greater or equal case)

    # Append the test case to asm_code
    asm_code.append( gen_br2_value_test( "blt", src0, src1, taken ) )
  
  return asm_code


#-------------------------------------------------------------------------
# gen_back_to_back_test
#-------------------------------------------------------------------------


# Test multiple consecutive blt instructions
def gen_back_to_back_test():
  return """
     # Test backwards walk (back to back branch taken)

     csrr x3, mngr2proc < -1      # Load a negative value into x3
     csrr x1, mngr2proc < 1       # Load positive value into x1

     blt  x3, x0, X0       # Branch if x3 < x0 (x3 is negative, so branch should be taken)
     csrw proc2mngr, x0    # Should not execute
     nop
     a0:
     csrw proc2mngr, x1 > 1
     blt  x3, x0, y0       # Backward branch if x3 < x0
     b0:
     blt  x3, x0, a0       # Backward branch if x3 < x0
     c0:
     blt  x3, x0, b0       # Backward branch if x3 < x0
     d0:
     blt  x3, x0, c0       # Backward branch if x3 < x0
     e0:
     blt  x3, x0, d0       # Backward branch if x3 < x0
     f0:
     blt  x3, x0, e0       # Backward branch if x3 < x0
     g0:
     blt  x3, x0, f0       # Backward branch if x3 < x0
     h0:
     blt  x3, x0, g0       # Backward branch if x3 < x0
     i0:
     blt  x3, x0, h0       # Backward branch if x3 < x0
     X0:
     blt  x3, x0, i0       # Forward branch if x3 < x0
     y0:

     blt  x3, x0, X1       # Repeat for second block of branches
     csrw proc2mngr, x0    # Should not execute
     nop
     a1:
     csrw proc2mngr, x1 > 1
     blt  x3, x0, y1       # Backward branch if x3 < x0
     b1:
     blt  x3, x0, a1       # Backward branch if x3 < x0
     c1:
     blt  x3, x0, b1       # Backward branch if x3 < x0
     d1:
     blt  x3, x0, c1       # Backward branch if x3 < x0
     e1:
     blt  x3, x0, d1       # Backward branch if x3 < x0
     f1:
     blt  x3, x0, e1       # Backward branch if x3 < x0
     g1:
     blt  x3, x0, f1       # Backward branch if x3 < x0
     h1:
     blt  x3, x0, g1       # Backward branch if x3 < x0
     i1:
     blt  x3, x0, h1       # Backward branch if x3 < x0
     X1:
     blt  x3, x0, i1       # Forward branch if x3 < x0
     y1:
     nop
     nop
     nop
     nop
     nop
     nop
     nop
  """