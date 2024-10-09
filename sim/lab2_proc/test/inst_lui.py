#=========================================================================
# lui
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
    lui x1, 0x0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 0x00001000
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

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------
# Test the destination register dependencies by varying how many nops are
# inserted after the instruction under test before reading the destination.

def gen_dest_dep_test():
  return [
    gen_imm_dest_dep_test( 5, "lui", 0x00000, 0x00000000 ),  # Load 0 -> 0x00000000
    gen_imm_dest_dep_test( 4, "lui", 0x00001, 0x00001000 ),  # Load 1 -> 0x00001000
    gen_imm_dest_dep_test( 3, "lui", 0xFFFFF, 0xFFFFF000 ),  # Load 0xFFFFF -> 0xFFFFF000
    gen_imm_dest_dep_test( 2, "lui", 0x7FFFF, 0x7FFFF000 ),  # Load 0x7FFFF -> 0x7FFFF000
    gen_imm_dest_dep_test( 1, "lui", 0x80000, 0x80000000 ),  # Load 0x80000 -> 0x80000000
    gen_imm_dest_dep_test( 0, "lui", 0x12345, 0x12345000 ),  # Load 0x12345 -> 0x12345000
  ]



#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_imm_value_test( "lui", 0x00000, 0x00000000 ),  # imm = 0 -> result should be 0
    gen_imm_value_test( "lui", 0x00001, 0x00001000 ),  # imm = 1 -> result should be 0x00001000
    gen_imm_value_test( "lui", 0xFFFFF, 0xFFFFF000 ),  # imm = 0xFFFFF -> result should be 0xFFFFF000
    gen_imm_value_test( "lui", 0x12345, 0x12345000 ),  # imm = 0x12345 -> result should be 0x12345000
    gen_imm_value_test( "lui", 0x80000, 0x80000000 ),  # imm = 0x80000 -> result should be 0x80000000
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    imm = random.randint(0, 0xFFFFF)  # 20-bit immediate for LUI
    result = imm << 12  # Shift left 12 bits as LUI does
    asm_code.append( gen_imm_value_test( "lui", imm, result ) )
  
  return asm_code
  
