#=========================================================================
# ProcDpathImmGen unit tests
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from lab2_proc.ProcDpathImmGen import ProcDpathImmGen

#-------------------------------------------------------------------------
# test I-type
#-------------------------------------------------------------------------

def test_immgen_i( cmdline_opts ):
  dut = ProcDpathImmGen()

  run_test_vector_sim( dut, [
    ('imm_type inst                                imm*'),
    [ 0,       0b11111111111100000000000000000000, 0b11111111111111111111111111111111],
    [ 0,       0b00000000000011111111111111111111, 0b00000000000000000000000000000000],
    [ 0,       0b01111111111100000000000000000000, 0b00000000000000000000011111111111],
    [ 0,       0b11111111111000000000000000000000, 0b11111111111111111111111111111110],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# test B-type
#-------------------------------------------------------------------------

def test_immgen_b( cmdline_opts ):
  dut = ProcDpathImmGen()

  run_test_vector_sim( dut, [
    ('imm_type inst                                imm*'),
    [ 2,       0b11111110000000000000111110000000, 0b11111111111111111111111111111110],
    [ 2,       0b00000001111111111111000001111111, 0b00000000000000000000000000000000],
    [ 2,       0b11000000000000000000111100000000, 0b11111111111111111111010000011110],
  ], cmdline_opts )

#'''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Add more tests for immediate types
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
