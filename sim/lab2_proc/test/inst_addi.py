#=========================================================================
# addi
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

    csrr x1, mngr2proc, < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x3, x1, 0x0004
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
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
    gen_rimm_dest_dep_test( 5, "addi", 0x00000f0f, 0x0ff, 0x0000100e ),
    gen_rimm_dest_dep_test( 4, "addi", 0x0000f0f0, 0xff0, 0x0000f0e0 ),
    gen_rimm_dest_dep_test( 3, "addi", 0x00000f0f, 0xf00, 0x00000e0f ),
    gen_rimm_dest_dep_test( 2, "addi", 0x0000f0f0, 0x00f, 0x0000f0ff ),
    gen_rimm_dest_dep_test( 1, "addi", 0x00000f0f, 0xfff, 0x00000f0e ),
    gen_rimm_dest_dep_test( 0, "addi", 0x0000f0f0, 0x0f0, 0x0000f1e0 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "addi", 0x00000f0f, 0x0ff, 0x0000100e ),
    gen_rimm_src_dep_test( 4, "addi", 0x0000f0f0, 0xff0, 0x0000f0e0 ),
    gen_rimm_src_dep_test( 3, "addi", 0x00000f0f, 0xf00, 0x00000e0f ),
    gen_rimm_src_dep_test( 2, "addi", 0x0000f0f0, 0xf0f, 0x0000efff ),
    gen_rimm_src_dep_test( 1, "addi", 0x00000f0f, 0xfff, 0x00000f0e ),
    gen_rimm_src_dep_test( 0, "addi", 0x0000f0f0, 0x0f0, 0x0000f1e0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "addi", 0x00000f0f, 0xff0, 0x00000eff ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "addi", 0xff00ff00, 0xf0f, 0xff00fe0f ),
    gen_rimm_value_test( "addi", 0x0ff00ff0, 0x0f0, 0x0ff010e0 ),
    gen_rimm_value_test( "addi", 0x00ff00ff, 0x00f, 0x00ff010e ),
    gen_rimm_value_test( "addi", 0xf00ff00f, 0xff0, 0xf00fefff ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = Bits32( random.randint(0, 0xffffffff) )
    imm = Bits12( random.randint(0, 0xfff) )
    # Sign-extend the immediate
    imm_sext = sext(imm, 32).int()
    dest = (src.int() + imm_sext) & 0xffffffff
    asm_code.append( gen_rimm_value_test( "addi", src.uint(), imm.uint(), dest ) )
  return asm_code