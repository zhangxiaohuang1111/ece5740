#=========================================================================
# bltu
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
    bltu   x2, x1, label_a
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
    gen_br2_src0_dep_test( 5, "bltu", 1, 7, True ),  # 1 < 7, branch taken
    gen_br2_src0_dep_test( 4, "bltu", 2, 7, True ),  
    gen_br2_src0_dep_test( 3, "bltu", 3, 7, True ),  
    gen_br2_src0_dep_test( 2, "bltu", 4, 7, True ),  
    gen_br2_src0_dep_test( 1, "bltu", 5, 7, True ),  
    gen_br2_src0_dep_test( 0, "bltu", 6, 7, True ),  
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bltu", 7, 1, False ),  # 7 >= 1, branch not taken
    gen_br2_src0_dep_test( 4, "bltu", 7, 2, False ),  
    gen_br2_src0_dep_test( 3, "bltu", 7, 3, False ),  
    gen_br2_src0_dep_test( 2, "bltu", 7, 4, False ),  
    gen_br2_src0_dep_test( 1, "bltu", 7, 5, False ),  
    gen_br2_src0_dep_test( 0, "bltu", 7, 6, False ),  
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu", 1, 7, True ),  # 1 < 7, branch taken
    gen_br2_src1_dep_test( 4, "bltu", 2, 7, True ),  
    gen_br2_src1_dep_test( 3, "bltu", 3, 7, True ),  
    gen_br2_src1_dep_test( 2, "bltu", 4, 7, True ),  
    gen_br2_src1_dep_test( 1, "bltu", 5, 7, True ),  
    gen_br2_src1_dep_test( 0, "bltu", 6, 7, True ),  
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu", 7, 1, False ),  # 7 >= 1, branch not taken
    gen_br2_src1_dep_test( 4, "bltu", 7, 2, False ),  
    gen_br2_src1_dep_test( 3, "bltu", 7, 3, False ),  
    gen_br2_src1_dep_test( 2, "bltu", 7, 4, False ),  
    gen_br2_src1_dep_test( 1, "bltu", 7, 5, False ),  
    gen_br2_src1_dep_test( 0, "bltu", 7, 6, False ),  
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu", 1, 2, True ),  # 1 < 2, branch taken
    gen_br2_srcs_dep_test( 4, "bltu", 2, 3, True ),  
    gen_br2_srcs_dep_test( 3, "bltu", 3, 4, True ),  
    gen_br2_srcs_dep_test( 2, "bltu", 4, 5, True ),  
    gen_br2_srcs_dep_test( 1, "bltu", 5, 6, True ),  
    gen_br2_srcs_dep_test( 0, "bltu", 6, 7, True ),  
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu", 2, 1, False ),  # 2 >= 1, branch not taken
    gen_br2_srcs_dep_test( 4, "bltu", 3, 2, False ),  
    gen_br2_srcs_dep_test( 3, "bltu", 4, 3, False ),  
    gen_br2_srcs_dep_test( 2, "bltu", 5, 4, False ),  
    gen_br2_srcs_dep_test( 1, "bltu", 6, 5, False ),  
    gen_br2_srcs_dep_test( 0, "bltu", 7, 6, False ),  
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bltu", 1, False ),  # src0 == src1, branch not taken
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "bltu", 0x00000000, 0x00000001, True  ),  # 0 < 1, branch taken
    gen_br2_value_test( "bltu", 0x00000001, 0x00000000, False ),  # 1 >= 0, branch not taken
    gen_br2_value_test( "bltu", 0x00000000, 0xFFFFFFFF, True  ),  # Unsigned comparison, 0 < 0xFFFFFFFF, branch taken
    gen_br2_value_test( "bltu", 0x7FFFFFFF, 0x80000000, True  ),  # Unsigned, 0x7FFFFFFF < 0x80000000, branch taken

    gen_br2_value_test( "bltu", 0xFFFFFFFF, 0xFFFFFFFF, False ),  # 0xFFFFFFFF == 0xFFFFFFFF, branch not taken
    gen_br2_value_test( "bltu", 0x00000000, 0x00000000, False ),  # 0 == 0, branch not taken

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

# Random test cases with bltu, covering both less, equal, and greater scenarios
def gen_random_test():
  asm_code = []
  for i in range(25):
    taken = random.choice([True, False])
    src0  = random.randint(0, 4294967295)  # Generate a 32-bit unsigned integer

    if taken:
      # Branch taken, src0 < src1 (unsigned comparison)
      src1 = random.randint(src0 + 1, 4294967295)  # Ensure src1 > src0
    else:
      # Branch not taken, src0 >= src1
      src1 = random.randint(0, src0)  # Ensure src0 >= src1

    # Append the test case to asm_code
    asm_code.append( gen_br2_value_test( "bltu", src0, src1, taken ) )
  
  return asm_code

#-------------------------------------------------------------------------
# gen_back_to_back_test
#-------------------------------------------------------------------------

# Test multiple consecutive bltu instructions with unsigned comparison (x0 < x3)
def gen_back_to_back_test():
  return """
     # Test backwards walk (back to back branch taken with unsigned comparison)

     csrr x3, mngr2proc < -1      # Load unsigned value into x3 (1)
     csrr x1, mngr2proc < 1      # Load unsigned value into x1 (1)

     bltu  x0, x3, X0           # If x0 < x3 (unsigned comparison), branch to X0
     csrw proc2mngr, x0         # If branch not taken, store x0 (this should not execute)
     nop
     a0:
     csrw proc2mngr, x1 > 1     # If branch taken, store x1 (which is 1)
     bltu  x0, x3, y0           # Backward branch if x0 < x3
     b0:
     bltu  x0, x3, a0           # Backward branch if x0 < x3
     c0:
     bltu  x0, x3, b0           # Backward branch if x0 < x3
     d0:
     bltu  x0, x3, c0           # Backward branch if x0 < x3
     e0:
     bltu  x0, x3, d0           # Backward branch if x0 < x3
     f0:
     bltu  x0, x3, e0           # Backward branch if x0 < x3
     g0:
     bltu  x0, x3, f0           # Backward branch if x0 < x3
     h0:
     bltu  x0, x3, g0           # Backward branch if x0 < x3
     i0:
     bltu  x0, x3, h0           # Backward branch if x0 < x3
     X0:
     bltu  x0, x3, i0           # Forward branch if x0 < x3
     y0:

     bltu  x0, x3, X1           # If x0 < x3 (unsigned comparison), branch to X1
     csrw proc2mngr, x0         # If branch not taken, store x0 (this should not execute)
     nop
     a1:
     csrw proc2mngr, x1 > 1     # If branch taken, store x1 (which is 1)
     bltu  x0, x3, y1           # Backward branch if x0 < x3
     b1:
     bltu  x0, x3, a1           # Backward branch if x0 < x3
     c1:
     bltu  x0, x3, b1           # Backward branch if x0 < x3
     d1:
     bltu  x0, x3, c1           # Backward branch if x0 < x3
     e1:
     bltu  x0, x3, d1           # Backward branch if x0 < x3
     f1:
     bltu  x0, x3, e1           # Backward branch if x0 < x3
     g1:
     bltu  x0, x3, f1           # Backward branch if x0 < x3
     h1:
     bltu  x0, x3, g1           # Backward branch if x0 < x3
     i1:
     bltu  x0, x3, h1           # Backward branch if x0 < x3
     X1:
     bltu  x0, x3, i1           # Forward branch if x0 < x3
     y1:
     nop
     nop
     nop
     nop
     nop
     nop
     nop
  """