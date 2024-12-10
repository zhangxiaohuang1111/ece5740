#=========================================================================
# extra multicore memory tests
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < {0x00002000,0x00002004,0x00002008,0x0000200c}
    csrr x2, mngr2proc < {0x0a0b0c0d,0x1a1b1c1d,0x2a2b2c2d,0x3a3b3c3d}
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sw   x2, 0(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw   x3, 0(x1)
    csrw proc2mngr, x3 > {0x0a0b0c0d,0x1a1b1c1d,0x2a2b2c2d,0x3a3b3c3d}

    .data
    .word 0x01020304
    .word 0x11121314
    .word 0x21222324
    .word 0x31323334
  """

def gen_shared_memory_test():
  return """
    csrr x1, mngr2proc < 0x00002000  # Base address
    csrr x2, mngr2proc < 0xdeadbeef  # Core 0 writes
    csrr x3, mngr2proc < 0xcafebabe  # Core 1 writes

    # Core 0 stores
    sw   x2, 0(x1)
    nop
    nop

    # Core 1 loads
    lw   x4, 0(x1)
    csrw proc2mngr, x4 > 0xdeadbeef  # Core 1 sees Core 0's value

    # Core 1 stores
    sw   x3, 0(x1)
    nop
    nop

    # Core 0 loads
    lw   x5, 0(x1)
    csrw proc2mngr, x5 > 0xcafebabe  # Core 0 sees Core 1's value

    .data
    .word 0x00000000
  """

def gen_unaligned_access_test():
  return """
    csrr x1, mngr2proc < 0x00002003  # Misaligned address
    csrr x2, mngr2proc < 0xdeadbeef

    # Attempt to store at unaligned address
    sw   x2, 0(x1)

    # Verify behavior (e.g., should raise exception or handle it)
    lw   x3, 0(x1)
    csrw proc2mngr, x3 > 0xdeadbeef

    .data
    .word 0x00000000
  """
def gen_concurrent_access_test():
  return """
    csrr x1, mngr2proc < 0x00002000
    csrr x2, mngr2proc < 0x12345678
    csrr x3, mngr2proc < 0x87654321

    # Core 0 writes
    sw   x2, 0(x1)
    nop
    nop

    # Core 1 reads
    lw   x4, 0(x1)
    csrw proc2mngr, x4 > 0x12345678

    # Core 1 writes
    sw   x3, 0(x1)
    nop
    nop

    # Core 0 reads
    lw   x5, 0(x1)
    csrw proc2mngr, x5 > 0x87654321

    .data
    .word 0x00000000
  """
def gen_random_test():
  asm_code = []
  base_addr = 0x00002000

  # Generate random store instructions
  for i in range(10):
    addr = base_addr + random.randint(0, 64)  # Random offset within range
    data = random.randint(0, 0xffffffff)      # Random 32-bit value
    asm_code.append(f"csrr x1, mngr2proc < {addr}")
    asm_code.append(f"csrr x2, mngr2proc < {data}")
    asm_code.append("sw x2, 0(x1)")

    # Random load and check
    asm_code.append(f"lw x3, 0(x1)")
    asm_code.append(f"csrw proc2mngr, x3 > {data}")

  asm_code.append(".data")
  asm_code.append(".word 0x00000000")  # Initialize memory
  return "\n".join(asm_code)

def gen_multicore_random_test():
  asm_code = []
  base_addr = 0x00002000

  # Core 0 random writes
  for i in range(5):
    addr = base_addr + random.randint(0, 64)
    data = random.randint(0, 0xffffffff)
    asm_code.append(f"csrr x1, mngr2proc < {addr}")
    asm_code.append(f"csrr x2, mngr2proc < {data}")
    asm_code.append("sw x2, 0(x1)")

  # Core 1 random reads
  for i in range(5):
    addr = base_addr + random.randint(0, 64)
    asm_code.append(f"csrr x3, mngr2proc < {addr}")
    asm_code.append("lw x4, 0(x3)")
    asm_code.append("nop")
    asm_code.append("csrw proc2mngr, x4 > x4")  # Just trace values

  asm_code.append(".data")
  asm_code.append(".word 0x00000000")
  return "\n".join(asm_code)

def gen_basic_random_test():
    base_addresses = [0x00002000 + i * 4 for i in range(4)]  # Generate base addresses
    random_values = [random.randint(0, 0xFFFFFFFF) for _ in range(4)]  # Generate random data

    asm_code = ""
    for addr, val in zip(base_addresses, random_values):
        asm_code += f"""
        csrr x1, mngr2proc < {hex(addr)}
        csrr x2, mngr2proc < {hex(val)}
        sw   x2, 0(x1)
        nop
        nop
        lw   x3, 0(x1)
        csrw proc2mngr, x3 > {hex(val)}
        """

    asm_code += """
    .data
    """
    # Add the random data to the .data section
    for _ in base_addresses:
        asm_code += ".word 0x00000000\n"

    return asm_code