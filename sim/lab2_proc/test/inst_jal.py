#=========================================================================
# jal
#=========================================================================

from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     # 0x0200
                        #
    nop                 # 0x0204
    nop                 # 0x0208
    nop                 # 0x020c
    nop                 # 0x0210
    nop                 # 0x0214
    nop                 # 0x0218
    nop                 # 0x021c
    nop                 # 0x0220
                        #
    jal   x1, label_a   # 0x0224
    addi  x3, x3, 0b01  # 0x0228

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
    csrw  proc2mngr, x1 > 0x0228

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10

  """

def gen_multijump_test():
  return """

    # Use x3 to track the control flow pattern
    addi  x3, x0, 0                # 0x00000200
    
    jal   x1, label_a              # 0x00000204
    addi  x3, x3, 0b000001         # 0x00000208

  label_b:
    addi  x3, x3, 0b000010         # 0x0000020c
    addi  x5, x1, 0                # 0x00000210
    jal   x1, label_c              # 0x00000214
    addi  x1, x3, 0b000100         # 0x00000218

  label_a:
    addi  x3, x3, 0b001000         # 0x0000021c
    addi  x4, x1, 0                # 0x00000220
    jal   x1, label_b              # 0x00000224
    addi  x3, x3, 0b010000         # 0x00000228

  label_c:
    addi  x3, x3, 0b100000         # 0x0000022c
    addi  x6, x1, 0                # 0x00000230

    # Carefully determine which bits are expected
    # to be set if jump operates correctly.
    csrw  proc2mngr, x3 > 0b101010

    # Check the link addresses
    csrw  proc2mngr, x4 > 0x00000208
    csrw  proc2mngr, x5 > 0x00000228
    csrw  proc2mngr, x6 > 0x00000218
  """
#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_5_test():
  return [
    gen_jump_dest_dep_test( 5, "jal", 0x228+2*4*5, 0x218+4*5 ),  
  ]

def gen_dest_dep_4_test():
  return [
    gen_jump_dest_dep_test( 4, "jal", 0x228+2*4*4, 0x218+4*4 ),  
  ]

def gen_dest_dep_3_test():
  return [
    gen_jump_dest_dep_test( 3, "jal", 0x228+2*4*3, 0x218+4*3 ),  
  ]

def gen_dest_dep_2_test():
  return [
    gen_jump_dest_dep_test( 2, "jal", 0x228+2*4*2, 0x218+4*2 ),
  ]

def gen_dest_dep_1_test():
  return [
    gen_jump_dest_dep_test( 1, "jal", 0x228+2*4*1, 0x218+4*1 ),
  ]

def gen_dest_dep_0_test():
  return [
    gen_jump_dest_dep_test( 0, "jal", 0x228, 0x218 ),
  ]

def gen_back_to_back_test():
  return """

    addi  x3, x0, 0                # 0x00000200
    jal   x1, label_d              # 0x00000204
    addi  x3, x3, 0b000001         # 0x00000208

  label_b:
    addi  x3, x3, 0b000010         # 0x0000020c
    addi  x6, x1, 0                # 0x00000210
    jal   x1, label_c              # 0x00000214
    addi  x1, x3, 0b000100         # 0x00000218

  label_a:
    addi  x3, x3, 0b001000         # 0x0000021c
    addi  x5, x1, 0                # 0x00000220
    jal   x1, label_b              # 0x00000224
    addi  x3, x3, 0b010000         # 0x00000228

  label_c:
    addi  x3, x3, 0b100000         # 0x0000022c
    addi  x7, x1, 0                # 0x00000230
    jal   x1, label_e              # 0x00000234
    addi  x3, x3, 0b100000         # 0x00000238


  label_d:
    addi  x3, x3, 0b110000         # 0x0000023c
    addi  x4, x1, 0                # 0x00000240
    jal   x1, label_a              # 0x00000244
    addi  x3, x3, 0b111000         # 0x00000248

  label_e:
    addi  x3, x3, 0b111100         # 0x0000024c
    addi  x8, x1, 0                # 0x00000250
    csrw  proc2mngr, x3 > 0x96

    csrw  proc2mngr, x4 > 0x00000208  # From 1 start
    csrw  proc2mngr, x5 > 0x00000248  # From 2 d-a
    csrw  proc2mngr, x6 > 0x00000228  # From 3 a-b
    csrw  proc2mngr, x7 > 0x00000218  # From 4 b-c
    csrw  proc2mngr, x8 > 0x00000238  # From 5 c-e
  """