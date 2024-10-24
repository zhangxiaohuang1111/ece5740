#=========================================================================
# complex_test.py
#=========================================================================
# This is a more comprehensive test that uses various instructions
# to cover different instruction categories including CSR, Reg-Reg,
# Reg-Imm, Memory, Jump, and Branch instructions.

from lab2_proc.test.harness import asm_test, run_test
from lab2_proc.ProcFL       import ProcFL
from lab2_proc.ProcBase     import ProcBase
from lab2_proc.ProcAlt      import ProcAlt

def test( cmdline_opts ):

  prog = """
    # Set up initial values using CSR instructions
    csrr  x1, mngr2proc < 10
    csrr  x2, mngr2proc < 20
    csrr  x3, mngr2proc < 30

    # Reg-Reg instructions
    add   x4, x1, x2       # x4 = 10 + 20=30
    sub   x5, x3, x1       # x5 = 30 - 10=20
    mul   x6, x1, x2       # x6 = 10 * 20=200
    and   x7, x1, x3       # x7 = 10 & 30=10
    or    x8, x2, x3       # x8 = 20 | 30=30
    xor   x9, x4, x5       # x9 = 30 ^ 20=10
    slt   x10, x1, x2      # x10 = (10 < 20)
    sltu  x11, x2, x3      # x11 = (20 <u 30)
    sra   x12, x3, x1      # x12 = 30 >> 10 (arithmetic)
    srl   x13, x2, x1      # x13 = 20 >> 10 (logical)
    sll   x14, x1, x2      # x14 = 10 << 20

    # Reg-Imm instructions
    addi  x15, x1, 5       # x15 = 10 + 5
    ori   x16, x2, 0x0F    # x16 = 20 | 0x0F
    andi  x17, x3, 0x0F    # x17 = 30 & 0x0F
    xori  x18, x4, 0xF0    # x18 = 30 ^ 0xF0
    slti  x19, x5, 25      # x19 = (20 < 25)
    sltiu x20, x6, 35      # x20 = (200 <u 35)
    srai  x21, x7, 2       # x21 = x7 >> 2 (arithmetic)
    srli  x22, x8, 1       # x22 = x8 >> 1 (logical)
    slli  x23, x9, 3       # x23 = x9 << 3
    lui   x24, 0x1000      # x24 = 0x10000000
    auipc x25, 0x2000      # x25 = PC + 0x20000000

    # Memory instructions
    sw    x10, 0(x1)       # Store x10 at address x1 + 0
    sw    x11, 4(x1)       # Store x11 at address x1 + 4
    lw    x26, 0(x1)       # Load from address x1 + 0 to x26
    lw    x27, 4(x1)       # Load from address x1 + 4 to x27

    # Jump to label1
    addi x3,x0,0
    lui   x1, %hi[label1]
    addi  x1, x1, %lo[label1]
    jalr  x28, x1, 0       # Jump to label1
    jal   x29, label8      # Jump to label8

  label1:
    addi  x3, x3, 1        # x3 += 1 (indicate label1 reached)

    # Jump to label2
    lui   x1, %hi[label3]
    addi  x1, x1, %lo[label3]
    jalr  x29, x1, 0       # Jump to label3
    #not reached
    jal   x29, label8      # Jump to label8
    addi  x3, x3, 1        # x3 += 2 (indicate label2 reached)


  label2:
    addi  x3, x3, 1        # x3 += 2 (indicate label2 reached)

    # Branch instructions
    beq   x26, x27, label7 # Branch if x26 == x27

    #not reached
    jal   x29, label8      # Jump to label8
    addi  x3, x3, 1        # x3 += 2 (indicate label2 reached)

    bge   x3, x1, label6   # Branch if x3 >= x1
    bltu  x2, x3, label7   # Branch if x2 <u x3
    bgeu  x3, x2, label8   # Branch if x3 >=u x2

  label3:
    addi  x4, x4, 3        # x4 += 3
    jal   x29, label2      # Jump to label2
  label4:
    addi  x5, x5, 4        # x5 += 4
    bne   x1, x2, label6   # Branch if x1 != x2
    #not reached
    jal   x29, label8      # Jump to label8
    addi  x3, x3, 1        # x3 += 2 (indicate label2 reached)


  label5:
    addi  x6, x6, 5        # x6 += 5
    #reached
    jal   x29, label8      # Jump to label8
    addi  x3, x3, 1        # x3 += 2 (indicate label2 reached)

  label6:
    addi  x7, x7, 6        # x7 += 6
    jal   x29, label5      # Jump to label5
    #not reached
    jal   x29, label8      # Jump to label8
    addi  x3, x3, 1        # x3 += 2 (indicate label2 reached)

  label7:
    addi  x8, x8, 7        # x8 += 7
    jal   x29, label4      # Jump to label4
    #not reached
    jal   x29, label8      # Jump to label8
    addi  x3, x3, 1        # x3 += 2 (indicate label2 reached)

  label8:
    addi  x9, x9, 8        # x9 += 8

    # Final result check using CSR
    csrw proc2mngr, x1 > 0x2bc   # x1 = 10
    csrw proc2mngr, x2 > 20   # x2 = 20
    csrw proc2mngr, x3 > 2   # x3 = 31
    csrw proc2mngr, x4 > 33   # x4 = 33
    csrw proc2mngr, x5 > 24   # x5 = 24
    csrw proc2mngr, x6 > 205  # x6 = 205
    csrw proc2mngr, x7 > 16   # x7 = 16
    csrw proc2mngr, x8 > 37   # x8 = 37
    csrw proc2mngr, x9 > 18   # x9 = 18
    csrw proc2mngr, x10 > 1   # x10 = 1
    csrw proc2mngr, x11 > 1   # x11 = 1
    csrw proc2mngr, x12 > 0   # x12 = 0
    csrw proc2mngr, x13 > 0   # x13 = 0
    csrw proc2mngr, x14 > 10485760  # x14 = 10485760
    csrw proc2mngr, x15 > 15  # x15 = 15
    csrw proc2mngr, x16 > 0x1f  # x16 = 0x1f
    csrw proc2mngr, x17 > 0xe  # x17 = 0xe
    csrw proc2mngr, x18 > 0xee # x18 = 0xee
    csrw proc2mngr, x19 > 1   # x19 = 1
    csrw proc2mngr, x20 > 0   # x20 = 0
    csrw proc2mngr, x21 > 2   # x21 = 2
    csrw proc2mngr, x22 > 15  # x22 = 15
    csrw proc2mngr, x23 > 80  # x23 = 80
    csrw proc2mngr, x24 > 0x1000000  # x24 = 0x10000000
  """
  # run_test( ProcFL, prog, cmdline_opts=cmdline_opts )
  # run_test( ProcBase, prog, cmdline_opts=cmdline_opts )
  # run_test( ProcAlt, prog, cmdline_opts=cmdline_opts )