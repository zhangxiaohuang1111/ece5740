#=========================================================================
# IntMulFL_test
#=========================================================================

import pytest

from random import randint

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from lab1_imul.IntMulFL import IntMulFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, imul ):

    # Instantiate models

    s.src  = StreamSourceFL( Bits64 )
    s.sink = StreamSinkFL( Bits32 )
    s.imul = imul

    # Connect

    s.src.ostream  //= s.imul.istream
    s.imul.ostream //= s.sink.istream

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.imul.line_trace() + " > " + s.sink.line_trace()

#-------------------------------------------------------------------------
# mk_imsg/mk_omsg
#-------------------------------------------------------------------------

# Make input message, truncate ints to ensure they fit in 32 bits.

def mk_imsg( a, b ):
  return concat( Bits32( a, trunc_int=True ), Bits32( b, trunc_int=True ) )

# Make output message, truncate ints to ensure they fit in 32 bits.

def mk_omsg( a ):
  return Bits32( a, trunc_int=True )

#----------------------------------------------------------------------
# Test Case: small positive * positive
#----------------------------------------------------------------------

small_pos_pos_msgs = [
  mk_imsg(  2,  3 ), mk_omsg(   6 ),
  mk_imsg(  4,  5 ), mk_omsg(  20 ),
  mk_imsg(  3,  4 ), mk_omsg(  12 ),
  mk_imsg( 10, 13 ), mk_omsg( 130 ),
  mk_imsg(  8,  7 ), mk_omsg(  56 ),
]

combine_zero_one_neg_msgs = [
  mk_imsg(  0,  3 ), mk_omsg(   0 ),
  mk_imsg(  4,  0 ), mk_omsg(   0 ),
  mk_imsg(  3, -4 ), mk_omsg( -12 ),
  mk_imsg( 2 , -13), mk_omsg(-26  ),
  mk_imsg( -1,  3 ), mk_omsg( -3  ),
  mk_imsg(  1, -7 ), mk_omsg(  -7 ),
  mk_imsg(  1, 23 ), mk_omsg(   23),
  mk_imsg(  1, 0  ), mk_omsg(   0 ),
  mk_imsg( -31, 0 ), mk_omsg(   0 ),

]

large_pos_neg_msgs = [
    mk_imsg( 23498934, -498230 ), mk_omsg( 23498934 * -498230),
    mk_imsg( 723945, -9812345  ), mk_omsg( 723945 * -9812345 ),
    mk_imsg( 398472, -9342     ), mk_omsg( 398472 * -9342    ),
    mk_imsg( -29384, 748923    ), mk_omsg( -29384 * 748923   ),
    mk_imsg( 92384, -2837      ), mk_omsg( 92384 * -2837     ),
]

masked_low_bits_msgs = [
    mk_imsg( 0xFFFFFFA3, 0x0000001C ), mk_omsg( 0xFFFFFFA3 * 0x0000001C ),
    mk_imsg( 0x00000092, 0xF1234567 ), mk_omsg( 0x00000092 * 0xF1234567 ),
]
masked_high_bits_msgs = [
    mk_imsg( 0x00123456, 0xF9876543 ), mk_omsg( 0x00123456 * 0xF9876543 ),
    mk_imsg( 0xF2345678, 0x00123456 ), mk_omsg( 0xF2345678 * 0x00123456 ),
]
sparse_number_msgs = [
    mk_imsg( 0b1000000000000100, 0b00000001 ), mk_omsg( 0b1000000000000100 * 0b00000001 ),
    mk_imsg( 0b1000000000010000, 0b00000010 ), mk_omsg( 0b1000000000010000 * 0b00000010 ),
]
dense_number_msgs = [
    mk_imsg( 0b1111111111111101, 0b00000010 ), mk_omsg( 0b1111111111111101 * 0b00000010 ),
    mk_imsg( 0b1111111111111111, 0b00000001 ), mk_omsg( 0b1111111111111111 * 0b00000001 ),
]


# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional lists of input/output messages to create
# additional directed and random test cases.
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                            src_delay sink_delay"),
  [ "small_pos_pos",        small_pos_pos_msgs,           2,        0          ],
  [ "combine_zero_one_neg", combine_zero_one_neg_msgs,    0,        0          ],
  [ "large_pos_neg",        large_pos_neg_msgs,           4,        0          ],
  [ "masked_low_bits",      masked_low_bits_msgs,         0,        0          ],
  [ "masked_high_bits",     masked_high_bits_msgs,        5,        3          ],
  [ "sparse_number",        sparse_number_msgs,           0,        0          ],
  [ "dense_number",         dense_number_msgs,            0,        3          ],

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to leverage the additional lists
  # of request/response messages defined above, but also to test
  # different source/sink random delays.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):

  th = TestHarness( IntMulFL() )

  th.set_param("top.src.construct",
    msgs=test_params.msgs[::2],
    initial_delay=test_params.src_delay+3,
    interval_delay=test_params.src_delay )

  th.set_param("top.sink.construct",
    msgs=test_params.msgs[1::2],
    initial_delay=test_params.sink_delay+3,
    interval_delay=test_params.sink_delay )

  run_sim( th, cmdline_opts, duts=['imul'] )

