#=========================================================================
# jalr
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

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0           # 0x0200
                              #
    lui x1,      %hi[label_a] # 0x0204
    addi x1, x1, %lo[label_a] # 0x0208
                              #
    nop                       # 0x020c
    nop                       # 0x0210
    nop                       # 0x0214
    nop                       # 0x0218
    nop                       # 0x021c
    nop                       # 0x0220
    nop                       # 0x0224
    nop                       # 0x0228
                              #
    jalr  x31, x1, 0          # 0x022c
    addi  x3, x3, 0b01        # 0x0230

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

    # Check the link address
    csrw  proc2mngr, x31 > 0x0230

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3  > 0b10

  """

def gen_dest_dep_5_test():
  return [
    gen_jalr_dest_dep_test( 0, 5, 'x31', '0x0210'),
  ]

def gen_dest_dep_4_test():
  return [
    gen_jalr_dest_dep_test( 0, 4, 'x31', '0x0210'),
  ]

def gen_dest_dep_3_test():
  return [
    gen_jalr_dest_dep_test( 0, 3, 'x31', '0x0210'),
  ]

def gen_dest_dep_2_test():
  return [
    gen_jalr_dest_dep_test( 0, 2, 'x31', '0x0210'),
  ]

def gen_dest_dep_1_test():
  return [
    gen_jalr_dest_dep_test( 0, 1, 'x31', '0x0210'),
  ]

def gen_dest_dep_0_test():
  return [
    gen_jalr_dest_dep_test( 0, 0, 'x31', '0x0210'),
  ]

def gen_src_dep_5_test():
  return [
    gen_jalr_src_dep_test( 5, 0, 'x31', 0x0210+5*4),
  ]

def gen_src_dep_4_test():
  return [
    gen_jalr_src_dep_test( 4, 0, 'x31', 0x0210+4*4),
  ]

def gen_src_dep_3_test():
  return [
    gen_jalr_src_dep_test( 3, 0, 'x31', 0x0210+3*4),
  ]

def gen_src_dep_2_test():
  return [
    gen_jalr_src_dep_test( 2, 0, 'x31', 0x0210+2*4),
  ]

def gen_src_dep_1_test():
  return [
    gen_jalr_src_dep_test( 1, 0, 'x31', 0x0210+1*4),
  ]

def gen_src_dep_0_test():
  return [
    gen_jalr_src_dep_test( 0, 0, 'x31', 0x0210),
  ]

def gen_src_eq_dest_test():
  return [
    gen_jalr_src_eq_dest_test( 0,0, 'x1', '0x0210'),
  ]

def gen_back_to_back_test():
  return """
    addi  x3, x0, 0                # 0x00000200
    
    lui   x1, %hi[label_d]         # 0x00000204
    addi  x1, x1, %lo[label_d]     # 0x00000208
    jalr  x2, x1, 0                # 0x0000020C
    addi  x3, x3, 0b000001         # 0x00000210

  label_b:
    addi  x3, x3, 0b000010         # 0x00000214
    addi  x6, x2, 0                # 0x00000218
    lui   x1, %hi[label_c]         # 0x0000021C
    addi  x1, x1, %lo[label_c]     # 0x00000220
    jalr  x2, x1, 0                # 0x00000224
    addi  x3, x3, 0b000100         # 0x00000228

  label_a:
    addi  x3, x3, 0b001000         # 0x0000022C
    addi  x5, x2, 0                # 0x00000230
    lui   x1, %hi[label_b]         # 0x00000234
    addi  x1, x1, %lo[label_b]     # 0x00000238
    jalr  x2, x1, 0                # 0x0000023C
    addi  x3, x3, 0b010000         # 0x00000240

  label_c:
    addi  x3, x3, 0b100000         # 0x00000244
    addi  x7, x2, 0                # 0x00000248
    lui   x1, %hi[label_e]         # 0x0000024C
    addi  x1, x1, %lo[label_e]     # 0x00000250
    jalr  x2, x1, 0                # 0x00000254
    addi  x3, x3, 0b100000         # 0x00000258

  label_d:
    addi  x3, x3, 0b110000         # 0x0000025C
    addi  x4, x2, 0                # 0x00000260
    lui   x1, %hi[label_a]         # 0x00000264
    addi  x1, x1, %lo[label_a]     # 0x00000268
    jalr  x2, x1, 0                # 0x0000026C
    addi  x3, x3, 0b111000         # 0x00000270

  label_e:
    addi  x3, x3, 0b111100         # 0x00000274
    addi  x8, x2, 0                # 0x00000278
    csrw  proc2mngr, x3 > 0x96     # 0x0000027C

    # Check return addresses
    csrw  proc2mngr, x4 > 0x00000210  # 
    csrw  proc2mngr, x5 > 0x00000270  # 
    csrw  proc2mngr, x6 > 0x00000240  # 
    csrw  proc2mngr, x7 > 0x00000228  # 
    csrw  proc2mngr, x8 > 0x00000258  # 
  """