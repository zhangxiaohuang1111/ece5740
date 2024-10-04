#=========================================================================
# bgeu
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
    bgeu   x1, x2, label_a
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

def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "bgeu", 7, 1, True ),  # 7 >= 1, branch taken
    gen_br2_src0_dep_test( 4, "bgeu", 7, 2, True ),
    gen_br2_src0_dep_test( 3, "bgeu", 7, 3, True ),
    gen_br2_src0_dep_test( 2, "bgeu", 7, 4, True ),
    gen_br2_src0_dep_test( 1, "bgeu", 7, 5, True ),
    gen_br2_src0_dep_test( 0, "bgeu", 7, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bgeu", 1, 7, False ),  # 1 < 7, branch not taken
    gen_br2_src0_dep_test( 4, "bgeu", 2, 7, False ),
    gen_br2_src0_dep_test( 3, "bgeu", 3, 7, False ),
    gen_br2_src0_dep_test( 2, "bgeu", 4, 7, False ),
    gen_br2_src0_dep_test( 1, "bgeu", 5, 7, False ),
    gen_br2_src0_dep_test( 0, "bgeu", 6, 7, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bgeu", 7, 1, True ),  # 7 >= 1, branch taken
    gen_br2_src1_dep_test( 4, "bgeu", 7, 2, True ),
    gen_br2_src1_dep_test( 3, "bgeu", 7, 3, True ),
    gen_br2_src1_dep_test( 2, "bgeu", 7, 4, True ),
    gen_br2_src1_dep_test( 1, "bgeu", 7, 5, True ),
    gen_br2_src1_dep_test( 0, "bgeu", 7, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bgeu", 1, 7, False ),  # 1 < 7, branch not taken
    gen_br2_src1_dep_test( 4, "bgeu", 2, 7, False ),
    gen_br2_src1_dep_test( 3, "bgeu", 3, 7, False ),
    gen_br2_src1_dep_test( 2, "bgeu", 4, 7, False ),
    gen_br2_src1_dep_test( 1, "bgeu", 5, 7, False ),
    gen_br2_src1_dep_test( 0, "bgeu", 6, 7, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bgeu", 2, 1, True ),  # 2 >= 1, branch taken
    gen_br2_srcs_dep_test( 4, "bgeu", 3, 2, True ),
    gen_br2_srcs_dep_test( 3, "bgeu", 4, 3, True ),
    gen_br2_srcs_dep_test( 2, "bgeu", 5, 4, True ),
    gen_br2_srcs_dep_test( 1, "bgeu", 6, 5, True ),
    gen_br2_srcs_dep_test( 0, "bgeu", 7, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bgeu", 1, 2, False ),  # 1 < 2, branch not taken
    gen_br2_srcs_dep_test( 4, "bgeu", 2, 3, False ),
    gen_br2_srcs_dep_test( 3, "bgeu", 3, 4, False ),
    gen_br2_srcs_dep_test( 2, "bgeu", 4, 5, False ),
    gen_br2_srcs_dep_test( 1, "bgeu", 5, 6, False ),
    gen_br2_srcs_dep_test( 0, "bgeu", 6, 7, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bgeu", 1, True ),  # src0 == src1, branch taken
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "bgeu", 0x00000001, 0x00000000, True  ),  # 1 >= 0
    gen_br2_value_test( "bgeu", 0x00000000, 0x00000001, False ),  # 0 < 1
    gen_br2_value_test( "bgeu", 0xFFFFFFFF, 0x00000000, True  ),  # Unsigned comparison, 0xFFFFFFFF >= 0
    gen_br2_value_test( "bgeu", 0x80000000, 0x7FFFFFFF, True  ),  # Unsigned, 0x80000000 >= 0x7FFFFFFF

    gen_br2_value_test( "bgeu", 0x00000000, 0x00000000, True  ),  # 0 == 0
    gen_br2_value_test( "bgeu", 0xFFFFFFFF, 0xFFFFFFFF, True  ),  # 0xFFFFFFFF == 0xFFFFFFFF

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

# Random test cases with bgeu, covering both greater, equal, and less scenarios
def gen_random_test():
  asm_code = []
  for i in range(25):
    taken = random.choice([True, False])
    src0  = random.randint(0, 4294967295)  # Generate a 32-bit unsigned integer

    if taken:
      # Branch taken, src0 >= src1 (includes both "greater" and "equal" cases)
      if random.choice([True, False]):  # Randomly decide between equal or greater case
        src1 = src0  # Equal case
      else:
        src1 = random.randint(0, src0)  # Greater or equal case
    else:
      # Branch not taken, src0 < src1 (unsigned comparison)
      src1 = random.randint(src0 + 1, 4294967295)  # src0 < src1, branch not taken

    # Append the test case to asm_code
    asm_code.append( gen_br2_value_test( "bgeu", src0, src1, taken ) )
  
  return asm_code

#-------------------------------------------------------------------------
# gen_back_to_back_test
#-------------------------------------------------------------------------

# Test multiple consecutive bgeu instructions
def gen_back_to_back_test():
  return """
     # Test backwards walk (back to back branch taken with unsigned comparison)

     csrr x3, mngr2proc < -1      # Load unsigned value into x3
     csrr x1, mngr2proc < 1      # Load unsigned value into x1

     bgeu  x3, x0, X0           # If x3 >= x0 (unsigned comparison), branch to X0
     csrw proc2mngr, x0         # If branch not taken, store x0 (this should not execute)
     nop
     a0:
     csrw proc2mngr, x1 > 1     # If branch taken, store x1 (which is 1)
     bgeu  x3, x0, y0           # Backward branch if x3 >= x0
     b0:
     bgeu  x3, x0, a0           # Backward branch if x3 >= x0
     c0:
     bgeu  x3, x0, b0           # Backward branch if x3 >= x0
     d0:
     bgeu  x3, x0, c0           # Backward branch if x3 >= x0
     e0:
     bgeu  x3, x0, d0           # Backward branch if x3 >= x0
     f0:
     bgeu  x3, x0, e0           # Backward branch if x3 >= x0
     g0:
     bgeu  x3, x0, f0           # Backward branch if x3 >= x0
     h0:
     bgeu  x3, x0, g0           # Backward branch if x3 >= x0
     i0:
     bgeu  x3, x0, h0           # Backward branch if x3 >= x0
     X0:
     bgeu  x3, x0, i0           # Forward branch if x3 >= x0
     y0:

     bgeu  x3, x0, X1           # If x3 >= x0 (unsigned comparison), branch to X1
     csrw proc2mngr, x0         # If branch not taken, store x0 (this should not execute)
     nop
     a1:
     csrw proc2mngr, x1 > 1     # If branch taken, store x1 (which is 1)
     bgeu  x3, x0, y1           # Backward branch if x3 >= x0
     b1:
     bgeu  x3, x0, a1           # Backward branch if x3 >= x0
     c1:
     bgeu  x3, x0, b1           # Backward branch if x3 >= x0
     d1:
     bgeu  x3, x0, c1           # Backward branch if x3 >= x0
     e1:
     bgeu  x3, x0, d1           # Backward branch if x3 >= x0
     f1:
     bgeu  x3, x0, e1           # Backward branch if x3 >= x0
     g1:
     bgeu  x3, x0, f1           # Backward branch if x3 >= x0
     h1:
     bgeu  x3, x0, g1           # Backward branch if x3 >= x0
     i1:
     bgeu  x3, x0, h1           # Backward branch if x3 >= x0
     X1:
     bgeu  x3, x0, i1           # Forward branch if x3 >= x0
     y1:
     nop
     nop
     nop
     nop
     nop
     nop
     nop
  """