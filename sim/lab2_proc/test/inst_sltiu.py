#=========================================================================
# sltiu
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sltiu x3, x1, 6
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
    csrr x1, mngr2proc < 10
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sltiu x3, x1, 11
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
    gen_rimm_dest_dep_test( 5, "sltiu",  10,          20,   1 ),
    gen_rimm_dest_dep_test( 4, "sltiu",  20,          10,   0 ),
    gen_rimm_dest_dep_test( 3, "sltiu",  4294967,     4095, 0 ),  
    gen_rimm_dest_dep_test( 2, "sltiu",  0,           4095, 1 ),   
    gen_rimm_dest_dep_test( 1, "sltiu",  429,         4000, 1 ),  
    gen_rimm_dest_dep_test( 0, "sltiu",  4294967,     1234, 0 ),  
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "sltiu",  10,         20,         1 ),
    gen_rimm_src_dep_test( 4, "sltiu",  20,         10,         0 ),
    gen_rimm_src_dep_test( 3, "sltiu",  4294967295, 0,          0 ),
    gen_rimm_src_dep_test( 2, "sltiu",  0,          4294967295, 1 ),
    gen_rimm_src_dep_test( 1, "sltiu",  4294967295, 4294967295, 1 ),
    gen_rimm_src_dep_test( 0, "sltiu",  4294967295, 4294967295, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "sltiu",  10,  20, 1 ),
    gen_rimm_src_eq_dest_test( "sltiu",  20,  10, 0 ),
    gen_rimm_src_eq_dest_test( "sltiu",  4294967295, 0, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    # Immediate is positive
    gen_rimm_value_test( "sltiu", 0x00000000, 0x000, 0 ),  # 0 < 0 -> False
    gen_rimm_value_test( "sltiu", 0x00000000, 0x001, 1 ),  # 0 < 1 -> True
    gen_rimm_value_test( "sltiu", 0x00000001, 0x001, 0 ),  # 1 < 1 -> False
    gen_rimm_value_test( "sltiu", 0x00000002, 0x001, 0 ),  # 2 < 1 -> False
    gen_rimm_value_test( "sltiu", 0xFFFFFFFF, 0x000, 0 ),  # 4294967295 < 0 -> False

    # Immediate is negative (sign-extended to a large unsigned value)
    gen_rimm_value_test( "sltiu", 0x00000000, 0xFFF, 1 ),  # 0 < 4294967295 -> True
    gen_rimm_value_test( "sltiu", 0xFFFFFFFF, 0xFFF, 0 ),  # 4294967295 < 4294967295 -> False
    gen_rimm_value_test( "sltiu", 0xFFFFFFFE, 0xFFF, 1 ),  # 4294967294 < 4294967295 -> True

    # Edge cases
    gen_rimm_value_test( "sltiu", 0x7FFFFFFF, 0x800, 1 ),  # 2147483647 < 4294965248 -> True
    gen_rimm_value_test( "sltiu", 0x80000000, 0x800, 1 ),  # 2147483648 < 4294965248 -> True
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = random.randint(0, 0xFFFFFFFF)
    imm_raw = random.randint(0, 0xFFF)
    imm_sext = sext(Bits12(imm_raw), 32)
    src_uint = src & 0xFFFFFFFF
    imm_sext_uint = imm_sext.uint()
    dest = 1 if src_uint < imm_sext_uint else 0
    asm_code.append( gen_rimm_value_test( "sltiu", src_uint, imm_raw, dest ) )
  return asm_code

