#=========================================================================
# ProcDpathAlu unit tests
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from lab2_proc.ProcDpathAlu import ProcDpathAlu

#-------------------------------------------------------------------------
# add
#-------------------------------------------------------------------------

def test_alu_add( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   0,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   0,  0x0ffbc964,   '?',      '?',       '?'      ],
    # pos-neg
    [ 0x00132050,   0xd6620040,   0,  0xd6752090,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   0,  0xfff0e890,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   0,  0xf353eaa3,   '?',      '?',       '?'      ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# sub
#-------------------------------------------------------------------------
def test_alu_sub( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim(dut, [
    ('in0          in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [0x00000000,   0x00000000,   1,  0x00000000,   '?',      '?',       '?'      ],
    
    #(p - p)
    [0x12345678,   0x0ABCDEF0,   1,  0x07777788,   '?',      '?',       '?'      ],
    [0x7FFFFFFF,   0x00000001,   1,  0x7FFFFFFE,   '?',      '?',       '?'      ],
    #(p - n)
    [0x12345678,   0xFEDCBA98,   1,  0x13579be0,   '?',      '?',       '?'      ],
    [0x7FFFFFFF,   0x80000000,   1,  0xFFFFFFFF,   '?',      '?',       '?'      ],
    #(n - p)
    [0x80000000,   0x00000001,   1,  0x7FFFFFFF,   '?',      '?',       '?'      ],
    [0xFEDCBA98,   0x12345678,   1,  0xeca86420,   '?',      '?',       '?'      ],
    #(n - n)
    [0x80000000,   0xFFFFFFFF,   1,  0x80000001,   '?',      '?',       '?'      ],
    [0xFFFFFFFF,   0x80000000,   1,  0x7FFFFFFF,   '?',      '?',       '?'      ],
    
  ], cmdline_opts)

#-------------------------------------------------------------------------
# AND
#-------------------------------------------------------------------------
def test_alu_and( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim(dut, [
    ('in0          in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [0x00000000,   0x00000000,   2,  0x00000000,   '?',      '?',       '?'      ],
    
    [0x12345678,   0x0ABCDEF0,   2,  0x02345670,   '?',      '?',       '?'      ],
    [0x7FFFFFFF,   0x00000001,   2,  0x00000001,   '?',      '?',       '?'      ],

    # (p & n)
    [0x12345678,   0xFEDCBA98,   2,  0x12141218,   '?',      '?',       '?'      ],
    [0x7FFFFFFF,   0x80000000,   2,  0x00000000,   '?',      '?',       '?'      ],

    # (n & p)
    [0x80000000,   0x00000001,   2,  0x00000000,   '?',      '?',       '?'      ],
    [0xFEDCBA98,   0x12345678,   2,  0x12141218,   '?',      '?',       '?'      ],

    # (n & n)
    [0x80000000,   0xFFFFFFFF,   2,  0x80000000,   '?',      '?',       '?'      ],
    [0xFFFFFFFF,   0x80000000,   2,  0x80000000,   '?',      '?',       '?'      ],
        
    
  ], cmdline_opts)


#-------------------------------------------------------------------------
# OR
#-------------------------------------------------------------------------
def test_alu_or( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim(dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    # (p | p)
    [0x00000000,   0x00000000,   3,  0x00000000,   '?',      '?',       '?'      ],
    [0x12345678,   0x0ABCDEF0,   3,  0x1abcdef8,   '?',      '?',       '?'      ],
    [0x7FFFFFFF,   0x00000001,   3,  0x7FFFFFFF,   '?',      '?',       '?'      ],
    
    # (p | n)
    [0x12345678,   0xFEDCBA98,   3,  0xfefcfef8,   '?',      '?',       '?'      ],
    [0x7FFFFFFF,   0x80000000,   3,  0xFFFFFFFF,   '?',      '?',       '?'      ],
    
    # (n | p)
    [0x80000000,   0x00000001,   3,  0x80000001,   '?',      '?',       '?'      ],
    [0xFEDCBA98,   0x12345678,   3,  0xfefcfef8,   '?',      '?',       '?'      ],
    
    # (n | n)
    [0x80000000,   0xFFFFFFFF,   3,  0xFFFFFFFF,   '?',      '?',       '?'      ],
    [0xFFFFFFFF,   0x80000000,   3,  0xFFFFFFFF,   '?',      '?',       '?'      ],
        
  ], cmdline_opts)

#-------------------------------------------------------------------------
# XOR
#-------------------------------------------------------------------------
def test_alu_xor( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim(dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    # (p ^ p)
    [0x00000000,   0x00000000,   4,  0x00000000,   '?',      '?',       '?'      ],
    [0x12345678,   0x0ABCDEF0,   4,  0x18888888,   '?',      '?',       '?'      ],
    [0x7FFFFFFF,   0x00000001,   4,  0x7FFFFFFE,   '?',      '?',       '?'      ],
    
    # (p ^ n)
    [0x12345678,   0xFEDCBA98,   4,  0xece8ece0,   '?',      '?',       '?'      ],
    [0x7FFFFFFF,   0x80000000,   4,  0xFFFFFFFF,   '?',      '?',       '?'      ],
    
    # (n ^ p)
    [0x80000000,   0x00000001,   4,  0x80000001,   '?',      '?',       '?'      ],
    [0xFEDCBA98,   0x12345678,   4,  0xece8ece0,   '?',      '?',       '?'      ],
    
    # (n ^ n)
    [0x80000000,   0xFFFFFFFF,   4,  0x7FFFFFFF,   '?',      '?',       '?'      ],
    [0xFFFFFFFF,   0x80000000,   4,  0x7FFFFFFF,   '?',      '?',       '?'      ],

  ], cmdline_opts)

#-------------------------------------------------------------------------
# SLT
#-------------------------------------------------------------------------
def test_alu_slt( cmdline_opts ):
    dut = ProcDpathAlu()

    run_test_vector_sim(dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    # Positive < Positive
    [0x00000001,   0x00000002,   5,  0x00000001,   '?',      '?',       '?'      ],
    [0x12345678,   0x12345679,   5,  0x00000001,   '?',      '?',       '?'      ],  # Similar positive values
    [0x7FFFFFFE,   0x7FFFFFFF,   5,  0x00000001,   '?',      '?',       '?'      ],  # Maximum positive values
    
    # Positive > Positive
    [0x00000002,   0x00000001,   5,  0x00000000,   '?',      '?',       '?'      ],
    [0x12345679,   0x12345678,   5,  0x00000000,   '?',      '?',       '?'      ],  
    [0x7FFFFFFF,   0x7FFFFFFE,   5,  0x00000000,   '?',      '?',       '?'      ],  
    # Negative < Positive
    [0xFFFFFFFF,   0x00000001,   5,  0x00000001,   '?',      '?',       '?'      ],
    [0xFFFFFFFE,   0x00000002,   5,  0x00000001,   '?',      '?',       '?'      ],  
    [0x80000000,   0x7FFFFFFF,   5,  0x00000001,   '?',      '?',       '?'      ],  
    # Negative > Negative
    [0xFFFFFFFE,   0xFFFFFFFF,   5,  0x00000001,   '?',      '?',       '?'      ],
    [0xFFFFFFFD,   0xFFFFFFFE,   5,  0x00000001,   '?',      '?',       '?'      ],  
    [0x80000001,   0x80000000,   5,  0x00000000,   '?',      '?',       '?'      ],  # Minimum negative + 1 vs minimum negativ
    # Positive < Negative
    [0x00000001,   0xFFFFFFFF,   5,  0x00000000,   '?',      '?',       '?'      ],
    [0x00000002,   0xFFFFFFFE,   5,  0x00000000,   '?',      '?',       '?'      ],  # Close positive and negative boundary
    [0x7FFFFFFF,   0x80000000,   5,  0x00000000,   '?',      '?',       '?'      ],  # Maximum positive vs minimum negativ
    # Equal numbers
    [0x80000000,   0x80000000,   5,  0x00000000,   '?',      '?',       '?'      ],
    [0x00000000,   0x00000000,   5,  0x00000000,   '?',      '?',       '?'      ],  # Zero values
    [0xFFFFFFFF,   0xFFFFFFFF,   5,  0x00000000,   '?',      '?',       '?'      ],  # Maximum negative equa
    # Negative < Negative
    [0x80000000,   0xFFFFFFFF,   5,  0x00000001,   '?',      '?',       '?'      ],
    [0x80000001,   0x80000002,   5,  0x00000001,   '?',      '?',       '?'      ],  # Close negative values
    [0x80000000,   0x80000001,   5,  0x00000001,   '?',      '?',       '?'      ],  # Minimum negative vs minimum negative + 1
  ], cmdline_opts)

#-------------------------------------------------------------------------
# SLTU
#-------------------------------------------------------------------------
def test_alu_sltu( cmdline_opts ):
    dut = ProcDpathAlu()

    run_test_vector_sim(dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    
    # Unsigned Positive < Unsigned Positive
    [0x00000001,   0x00000002,   6,  0x00000001,   '?',      '?',       '?'      ],
    [0x12345678,   0xFFFFFFFF,   6,  0x00000001,   '?',      '?',       '?'      ],  
    
    # Unsigned Positive > Unsigned Positive
    [0x00000002,   0x00000001,   6,  0x00000000,   '?',      '?',       '?'      ],
    [0xFFFFFFFF,   0x12345678,   6,  0x00000000,   '?',      '?',       '?'      ],  
    
    # Unsigned Equal
    [0x00000001,   0x00000001,   6,  0x00000000,   '?',      '?',       '?'      ],
    [0xFFFFFFFF,   0xFFFFFFFF,   6,  0x00000000,   '?',      '?',       '?'      ],
    
    # Zero < Unsigned Positive
    [0x00000000,   0x00000001,   6,  0x00000001,   '?',      '?',       '?'      ],
    [0x00000000,   0xFFFFFFFF,   6,  0x00000001,   '?',      '?',       '?'      ],
    # Maximum Unsigned vs. Zero
    [0xFFFFFFFF,   0x00000000,   6,  0x00000000,   '?',      '?',       '?'      ],
    [0x00000000,   0xFFFFFFFF,   6,  0x00000001,   '?',      '?',       '?'      ],  # Zero < Maximum Unsigned
  
  ], cmdline_opts)
    

#-------------------------------------------------------------------------
# SRA
#-------------------------------------------------------------------------
def test_alu_sra( cmdline_opts ):
    dut = ProcDpathAlu()

    run_test_vector_sim(dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    # Shift by 0 (no shift, result should be the same as in0)
    [0x00000001,   0x00000000,   7,  0x00000001,   '?',      '?',       '?'      ],  # Small positive number
    [0x80000000,   0x00000000,   7,  0x80000000,   '?',      '?',       '?'      ],  # Large negative number (MSB remains
    # Shift small positive number by 1, 2, 3, etc.
    [0x00000001,   0x00000001,   7,  0x00000000,   '?',      '?',       '?'      ],  # Shift by 1
    [0x00000008,   0x00000002,   7,  0x00000002,   '?',      '?',       '?'      ],  # Shift by 2
    [0x00000010,   0x00000003,   7,  0x00000002,   '?',      '?',       '?'      ],  # Shift by 3
    
    # Shift large positive number by various positions
    [0x7FFFFFFF,   0x00000001,   7,  0x3FFFFFFF,   '?',      '?',       '?'      ],  # Shift by 1
    [0x7FFFFFFF,   0x00000005,   7,  0x03FFFFFF,   '?',      '?',       '?'      ],  # Shift by 5
    
    # Shift large negative number (signed shift should propagate the sign bit)
    [0x80000000,   0x00000001,   7,  0xC0000000,   '?',      '?',       '?'      ],  # Shift by 1 (propagate MSB)
    [0x80000000,   0x0000001F,   7,  0xFFFFFFFF,   '?',      '?',       '?'      ],  # Shift by 31 (maximum shift)
    
    # Shift negative numbers (sign extension should happen)
    [0xFFFFFFFF,   0x00000004,   7,  0xFFFFFFFF,   '?',      '?',       '?'      ],  # Shift by 4 (all 1's remain)
    [0xFFFFFFFE,   0x00000002,   7,  0xFFFFFFFF,   '?',      '?',       '?'      ],  # Shift by 2 (propagate MSB)
    
    # Shifting with in1 values beyond 5 bits (in1[4:0] = 0x1F)
    [0x12345678,   0x0000003F,   7,  0x00000000,   '?',      '?',       '?'      ],  # Shifting more than 31 (all zeros)
    [0x80000000,   0x0000003F,   7,  0xFFFFFFFF,   '?',      '?',       '?'      ],  # Maximum shift for negative (all ones
    # Edge case with shift of 31
    [0x00000001,   0x0000001F,   7,  0x00000000,   '?',      '?',       '?'      ],  # Shift 1 bit number by 31 (result = 0)
    [0x80000000,   0x0000001F,   7,  0xFFFFFFFF,   '?',      '?',       '?'      ],  # Shift by 31 for large negative

  ], cmdline_opts)


#-------------------------------------------------------------------------
# SRL
#-------------------------------------------------------------------------
def test_alu_srl( cmdline_opts ):
    dut = ProcDpathAlu()

    run_test_vector_sim(dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    # Shift by 0 (no shift, result should be the same as in0)
    [0x00000001,   0x00000000,   8,  0x00000001,   '?',      '?',       '?'      ],  # Small positive number
    [0x80000000,   0x00000000,   8,  0x80000000,   '?',      '?',       '?'      ],  # Large number (MSB remains, no shift)
    [0xFFFFFFFF,   0x00000000,   8,  0xFFFFFFFF,   '?',      '?',       '?'      ],  # All bits set (no shift
    # Shift small positive number by 1, 2, 3, etc.
    [0x00000001,   0x00000001,   8,  0x00000000,   '?',      '?',       '?'      ],  # Shift by 1
    [0x00000008,   0x00000002,   8,  0x00000002,   '?',      '?',       '?'      ],  # Shift by 2
    [0x00000010,   0x00000003,   8,  0x00000002,   '?',      '?',       '?'      ],  # Shift by 
    # Shift large positive number by various positions
    [0x7FFFFFFF,   0x00000001,   8,  0x3FFFFFFF,   '?',      '?',       '?'      ],  # Shift by 1
    [0x7FFFFFFF,   0x00000005,   8,  0x03FFFFFF,   '?',      '?',       '?'      ],  # Shift by 5
    [0x7FFFFFFF,   0x0000001F,   8,  0x00000000,   '?',      '?',       '?'      ],  # Shift by 31 (max shift
    # Shift large negative number (considered unsigned in SRL, no sign extension)
    [0x80000000,   0x00000001,   8,  0x40000000,   '?',      '?',       '?'      ],  # Shift by 1
    [0x80000000,   0x0000001F,   8,  0x00000001,   '?',      '?',       '?'      ],  # Shift by 31 (max shift
    # Shift negative numbers (no sign extension)
    [0xFFFFFFFF,   0x00000004,   8,  0x0FFFFFFF,   '?',      '?',       '?'      ],  # Shift by 4 (logical shift)
    [0xFFFFFFFE,   0x00000002,   8,  0x3FFFFFFF,   '?',      '?',       '?'      ],  # Shift by 2 (logical shift
    # Shifting with in1 values beyond 5 bits (in1[4:0] = 0x1F)
    [0x12345678,   0x0000003F,   8,  0x00000000,   '?',      '?',       '?'      ],  # Shift 31 (larger shifts only use 5 bits)
    [0x80000000,   0x0000003F,   8,  0x00000001,   '?',      '?',       '?'      ],  # Maximum shift for large numbe
    # Edge case with shift of 31
    [0x00000001,   0x0000001F,   8,  0x00000000,   '?',      '?',       '?'      ],  # Shift 1 bit number by 31 (result = 0)
    [0x80000000,   0x0000001F,   8,  0x00000001,   '?',      '?',       '?'      ],  # Shift 31 for large number (MSB becomes LSB)

  ], cmdline_opts)
    

#-------------------------------------------------------------------------
# SLL
#-------------------------------------------------------------------------
def test_alu_sll( cmdline_opts ):
    dut = ProcDpathAlu()

    run_test_vector_sim(dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    # Shift by 0 (no shift, result should be the same as in0)
    [0x00000001,   0x00000000,   9,  0x00000001,   '?',      '?',       '?'      ],  # Small positive number
    [0x80000000,   0x00000000,   9,  0x80000000,   '?',      '?',       '?'      ],  # Large negative number
    [0xFFFFFFFF,   0x00000000,   9,  0xFFFFFFFF,   '?',      '?',       '?'      ],  # All bits set (no shift
    # Shift small positive numbers by 1, 2, 3, etc.
    [0x00000001,   0x00000001,   9,  0x00000002,   '?',      '?',       '?'      ],  # Shift by 1
    [0x00000001,   0x00000004,   9,  0x00000010,   '?',      '?',       '?'      ],  # Shift by 4
    [0x00000003,   0x00000005,   9,  0x00000060,   '?',      '?',       '?'      ],  # Shift by 
    # Shift large positive number by various positions
    [0x7FFFFFFF,   0x00000001,   9,  0xFFFFFFFE,   '?',      '?',       '?'      ],  # Shift by 1
    [0x7FFFFFFF,   0x00000004,   9,  0xFFFFFFF0,   '?',      '?',       '?'      ],  # Shift by 4
    [0x7FFFFFFF,   0x0000001F,   9,  0x80000000,   '?',      '?',       '?'      ],  # Shift by 31 (only MSB left
    # Shift large negative number by various positions
    [0x80000000,   0x00000001,   9,  0x00000000,   '?',      '?',       '?'      ],  # Shift by 1 (MSB shifted out)
    [0x80000000,   0x0000001F,   9,  0x00000000,   '?',      '?',       '?'      ],  # Shift by 31 (all bits shifted out
    # Shift negative numbers (no sign extension, logical shift)
    [0xFFFFFFFF,   0x00000001,   9,  0xFFFFFFFE,   '?',      '?',       '?'      ],  # Shift by 1
    [0xFFFFFFFF,   0x00000004,   9,  0xFFFFFFF0,   '?',      '?',       '?'      ],  # Shift by 4
    [0xFFFFFFFE,   0x00000002,   9,  0xFFFFFFF8,   '?',      '?',       '?'      ],  # Shift by 
    # Shifting with in1 values beyond 5 bits (in1[4:0] = 0x1F)
    [0x12345678,   0x0000003F,   9,  0x00000000,   '?',      '?',       '?'      ],  # Shifting by large amounts
    [0x00000001,   0x0000003F,   9,  0x80000000,   '?',      '?',       '?'      ],  # Shift by 31 (only MSB left
    # Edge cases
    [0x00000001,   0x0000001F,   9,  0x80000000,   '?',      '?',       '?'      ],  # Shift by 31 (result should be MSB)
    [0xFFFFFFFF,   0x0000001F,   9,  0x80000000,   '?',      '?',       '?'      ],  # Shift by 31 (negative, all 1s -> MSB)
    [0x80000000,   0x0000001F,   9,  0x00000000,   '?',      '?',       '?'      ],  # Negative, shift out MSB, result = 0

  ], cmdline_opts)


#-------------------------------------------------------------------------
# JALR
#-------------------------------------------------------------------------
def test_alu_JALR( cmdline_opts ):
    dut = ProcDpathAlu()

    run_test_vector_sim(dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    # Zero + Zero
    [0x00000000,   0x00000000,   10, 0x00000000,   '?',      '?',       '?'      ],  # Result should be 0, LSB already 
    # Positive + Positive
    [0x00000002,   0x00000003,   10, 0x00000004,   '?',      '?',       '?'      ],  # 5 & 32'hfffffffe = 4
    [0x00000010,   0x00000001,   10, 0x00000010,   '?',      '?',       '?'      ],  # 17 & 32'hfffffffe = 16
    
    # Positive + Negative
    [0x00000010,   0xFFFFFFF0,   10, 0x00000000,   '?',      '?',       '?'      ],  # (16 + (-16)) & 32'hfffffffe = 0
    [0x7FFFFFFF,   0x80000001,   10, 0x00000000,   '?',      '?',       '?'      ],  # (INT_MAX + INT_MIN) & 32'hfffffffe = 
    # Negative + Negative
    [0xFFFFFFFF,   0xFFFFFFFF,   10, 0xFFFFFFFE,   '?',      '?',       '?'      ],  # (-1 + -1) & 32'hfffffffe = -2
    [0x80000000,   0x80000000,   10, 0x00000000,   '?',      '?',       '?'      ],  # Overflow check: (-2^31 + -2^31) & 32'hfffffffe = 
    # Overflow scenarios
    [0x7FFFFFFF,   0x00000001,   10, 0x80000000,   '?',      '?',       '?'      ],  # (2^31-1 + 1) -> Overflow but mask LSB
    [0x80000000,   0xFFFFFFFF,   10, 0x7FFFFFFE,   '?',      '?',       '?'      ],  # (-2^31 + (-1)) & 32'hfffffffe = 7FFFFFF
    # Boundary cases (max and min values)
    [0x00000001,   0xFFFFFFFF,   10, 0x00000000,   '?',      '?',       '?'      ],  # (1 + (-1)) & 32'hfffffffe = 0
    [0xFFFFFFFF,   0x00000001,   10, 0x00000000,   '?',      '?',       '?'      ],  # (-1 + 1) & 32'hfffffffe = 0
    [0x80000000,   0x00000001,   10, 0x80000000,   '?',      '?',       '?'      ],  # (-2^31 + 1) & 32'hfffffffe = 8000000
    # Ensure LSB is cleared
    [0x00000001,   0x00000002,   10, 0x00000002,   '?',      '?',       '?'      ],  # 3 & 32'hfffffffe = 2
    [0x12345678,   0x87654321,   10, 0x99999998,   '?',      '?',       '?'      ],  # Add and mask LS
    # Large positive values
    [0x7FFFFFFF,   0x7FFFFFFF,   10, 0xFFFFFFFE,   '?',      '?',       '?'      ],  # Overflow, LSB should be cleared

  ], cmdline_opts)

#-------------------------------------------------------------------------
# cp_op0
#-------------------------------------------------------------------------

def test_alu_cp_op0( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  11,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  11,  0x0ffaa660,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  11,  0x00132050,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  11,  0xfff0a440,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  11,  0xfeeeeaa3,   '?',      '?',       '?'      ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# cp_op1
#-------------------------------------------------------------------------

def test_alu_cp_op1( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  12,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  12,  0x00012304,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  12,  0xd6620040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  12,  0x00004450,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  12,  0xf4650000,   '?',      '?',       '?'      ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# cp_equality
#-------------------------------------------------------------------------

def test_alu_fn_equality( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  13,  0x00000000,   1,        '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  13,  0x00000000,   0,        '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  13,  0x00000000,   0,        '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  13,  0x00000000,   0,        '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  13,  0x00000000,   0,        '?',       '?'      ],
  ], cmdline_opts )

