#=========================================================================
# auipc
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
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
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
# Test destination register dependency with various delays.
# We test how the destination register handles different delays between
# instruction execution and reading the result.

def gen_dest_dep_test():
    return [
        # AUIPC with imm = 0x00010, result should be PC + (0x00010 << 12)
        gen_imm_dest_dep_test(5, "auipc", 0x00010, 0x200 + (0x00010 << 12)),

        # AUIPC with imm = 0xFFFFF, result should be PC + (0xFFFFF << 12)
        gen_imm_dest_dep_test(4, "auipc", 0xFFFFF, 0x200+4*5+8 + (0xFFFFF << 12)),

        # AUIPC with imm = 0x00000, result should be PC + (0 << 12)
        gen_imm_dest_dep_test(3, "auipc", 0x00001, 0x21c+4*4+8 + (0x00001 << 12)),

        # AUIPC with imm = 0x12345, result should be PC + (0x12345 << 12)
        gen_imm_dest_dep_test(2, "auipc", 0x12345, 0x21c+4*4+8+3*4+8 + (0x12345 << 12)),

        # AUIPC with imm = 0x80000, result should be PC + (0x80000 << 12)
        gen_imm_dest_dep_test(1, "auipc", 0x80000, 0x21c+4*4+8+3*4+8+2*4+8 + (0x80000 << 12)),
    ]
#-------------------------------------------------------------------------
# gen_auipc_value_test
#-------------------------------------------------------------------------
# Testing specific values for correctness of the AUIPC instruction.

def gen_value_test():
    return [
        # Test 1: AUIPC with imm = 1, result should be PC + (1 << 12)
        gen_imm_value_test( "auipc", 0x00001, 0x200 + (0x00001 << 12)),  # PC + (1 << 12)

        # Test 2: AUIPC with imm = 0xFFFFF, result should be PC + (0xFFFFF << 12)
        gen_imm_value_test( "auipc", 0xFFFFF, 0x208 + (0xFFFFF << 12)),  # PC + (0xFFFFF << 12)

        # Test 3: AUIPC with imm = 0x00000, result should be PC + (0x00000 << 12) (same as PC)
        gen_imm_value_test( "auipc", 0x00000, 0x210 + (0x00000 << 12)),  # PC + (0 << 12)

        # Test 4: AUIPC with imm = 0x12345, result should be PC + (0x12345 << 12)
        gen_imm_value_test( "auipc", 0x12345, 0x218 + (0x12345 << 12)),  # PC + (0x12345 << 12)

        # Test 5: AUIPC with imm = 0x80000, result should be PC + (0x80000 << 12)
        gen_imm_value_test( "auipc", 0x80000, 0x220 + (0x80000 << 12)),  # PC + (0x80000 << 12)
    ]


#-------------------------------------------------------------------------
# gen_auipc_random_test
#-------------------------------------------------------------------------
# Generate random test cases for AUIPC.
# PC starts at a base of 0x200, and immediate values are randomized.

def gen_auipc_random_test():
    asm_code = []
    pc_base = 0x200  # Assume PC starts at 0x200

    for i in range(100):
        imm = random.randint(0, 0xFFFFF)  # Generate a random 20-bit immediate value
        pc_offset = pc_base + (i * 8)  # Increment PC offset for each iteration
        result = pc_offset + (imm << 12)  # PC + (imm << 12)

        # Append the randomly generated test case
        asm_code.append(gen_imm_value_test("auipc", imm, result))
    
    return asm_code