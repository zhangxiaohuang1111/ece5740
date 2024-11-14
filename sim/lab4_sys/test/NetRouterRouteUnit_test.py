#=========================================================================
# NetRouterRouteUnit_test
#=========================================================================

import pytest

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from lab4_sys.NetMsg import mk_net_msg
from lab4_sys.NetRouterRouteUnit import NetRouterRouteUnit

#-------------------------------------------------------------------------
# Message Types
#-------------------------------------------------------------------------

NetMsgType = mk_net_msg( 32 )

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, router_id=0 ):

    # Instantiate models

    s.src   = StreamSourceFL( NetMsgType )
    s.runit = NetRouterRouteUnit( p_msg_nbits=44 )
    s.sinks = [ StreamSinkFL( NetMsgType ) for _ in range(3) ]

    # Connect

    s.runit.router_id  //= router_id
    s.src.ostream      //= s.runit.istream
    s.runit.ostream[0] //= s.sinks[0].istream
    s.runit.ostream[1] //= s.sinks[1].istream
    s.runit.ostream[2] //= s.sinks[2].istream

  def done( s ):
    return s.src.done() and s.sinks[0].done() and s.sinks[1].done() and s.sinks[2].done()

  def line_trace( s ):
    return s.src.line_trace()   + " > (" + \
           s.runit.line_trace() + ") > " + \
           s.sinks[0].line_trace() + "|" + \
           s.sinks[1].line_trace() + "|" + \
           s.sinks[2].line_trace()

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------
# This is an example of a basic test. This test may not be valid
# depending on your routing algorithm. You are free to change this test.
# We will not test your route unit since its functionality depends on the
# chosen routing algorithm.

def test_basic( cmdline_opts ):

  th = TestHarness( router_id=0 )

  msgs = [
    #           src  dest opaq  payload
    NetMsgType( 0,   0,   0x10, 0x10101010 ),
    NetMsgType( 0,   1,   0x11, 0x11111111 ),
    NetMsgType( 0,   2,   0x12, 0x12121212 ),
    NetMsgType( 0,   3,   0x13, 0x13131313 ),
  ]

  th.set_param("top.src.construct",   msgs=msgs  )
  th.set_param("top.sinks[0].construct", msgs=[ m for m in msgs if m.dest == 0 ] )
  th.set_param("top.sinks[1].construct", msgs=[ m for m in msgs if m.dest != 0 ] )
  th.set_param("top.sinks[2].construct", msgs=[] )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['runit'] )

#-------------------------------------------------------------------------
# Test Cases: Very Simple
#-------------------------------------------------------------------------
# These are examples of a simple tests using a test case table. These
# tests may not be valid depending on your routing algorithm. You are
# free to change these tests. We will not test your route unit since its
# functionality depends on the chosen routing algorithm.

one = [
  #           src  dest opaq  payload
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
]

four = [
  #           src  dest opaq  payload
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
  NetMsgType( 0,   1,   0x11, 0x11111111 ),
  NetMsgType( 0,   2,   0x12, 0x12121212 ),
  NetMsgType( 0,   3,   0x13, 0x13131313 ),
]

four_diff_src = [
  #           src  dest opaq  payload
  NetMsgType( 3,   0,   0x10, 0x10101010 ),
  NetMsgType( 2,   1,   0x11, 0x11111111 ),
  NetMsgType( 1,   2,   0x12, 0x12121212 ),
  NetMsgType( 0,   3,   0x13, 0x13131313 ),
]

#''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Change above tests if necessary; add more directed tests
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                              "msgs          src_delay sink_delay delay_mode"),
  [ "one",                        one,                 0,  0,  'fixed'  ],
  [ "four",                       four,                0,  0,  'fixed'  ],
  [ "four_diff_src",              four_diff_src,       0,  0,  'fixed'  ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

#-------------------------------------------------------------------------
# test w/ router id 0
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test_router_id_0( test_params, cmdline_opts ):

  th = TestHarness( router_id=0 )

  th.set_param("top.src.construct",
    msgs                = test_params.msgs,
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.sinks[0].construct",
    msgs                = [ m for m in test_params.msgs if m.dest == 0 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[1].construct",
    msgs                = [ m for m in test_params.msgs if m.dest != 0 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.set_param("top.sinks[2].construct",
    msgs                = [],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['runit'] )

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

