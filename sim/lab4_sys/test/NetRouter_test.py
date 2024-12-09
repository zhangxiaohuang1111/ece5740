#=========================================================================
# NetRouter_test
#=========================================================================

import pytest

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from lab4_sys.NetMsg import mk_net_msg
from lab4_sys.NetRouter import NetRouter

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

    s.srcs   = [ StreamSourceFL( NetMsgType ) for _ in range(3) ]
    s.router = NetRouter( p_msg_nbits=44 )
    s.sinks  = [ StreamSinkFL( NetMsgType ) for _ in range(3) ]

    # Connect

    s.router.router_id //= router_id
    for i in range(3):
      s.srcs[i].ostream   //= s.router.istream[i]
      s.router.ostream[i] //= s.sinks[i].istream

  def done( s ):
    for i in range(3):
      if not s.srcs[i].done() or not s.sinks[i].done():
        return False
    return True

  def line_trace( s ):
    srcs_str  = "|".join([ src.line_trace()  for src  in s.srcs  ])
    sinks_str = "|".join([ sink.line_trace() for sink in s.sinks ])
    return f"{srcs_str} > ({s.router.line_trace()}) > {sinks_str}"

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------
# These is an example of a basic test. This tests may not be valid
# depending on your routing and arbitration algorithms. You are free to
# change this test. We will not test your router since its functionality
# depends on the chosen routing and arbitration algorithms.

def test_basic( cmdline_opts ):

  th = TestHarness(router_id=0)

  msgs = [
    #           src  dest opaq  payload
    NetMsgType( 1,   0,   0x10, 0x10101010 ),
    NetMsgType( 2,   1,   0x11, 0x11111111 ),
    NetMsgType( 0,   2,   0x12, 0x12121212 ),
  ]
  router_id = 0

  msgs_to_sink_0 = [
  m for m in msgs
  if m.dest != router_id and ((m.dest - router_id) & 3) >= ((router_id - m.dest) & 3)
  ]  # Left
  msgs_to_sink_1 = [
  m for m in msgs
  if m.dest != router_id and ((m.dest - router_id) & 3) < ((router_id - m.dest) & 3)
  ]  # Right
  msgs_to_sink_2 = [m for m in msgs if m.dest == router_id] # Local

  th.set_param("top.srcs[0].construct",  msgs=[ m for m in msgs if m.src  == 0 ] )
  th.set_param("top.srcs[1].construct",  msgs=[ m for m in msgs if m.src  == 1 ] )
  th.set_param("top.srcs[2].construct",  msgs=[ m for m in msgs if m.src  == 2 ] )
  th.set_param("top.sinks[0].construct", msgs=msgs_to_sink_0)
  th.set_param("top.sinks[1].construct", msgs=msgs_to_sink_1)
  th.set_param("top.sinks[2].construct", msgs=msgs_to_sink_2)

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['router'] )

#-------------------------------------------------------------------------
# Test Cases: Very Simple
#-------------------------------------------------------------------------
# These are examples of a simple tests using a test case table. These
# tests may not be valid depending on your routing and arbitration
# algorithms. You are free to change these tests. We will not test your
# switch unit since its functionality depends on the chosen routing and
# arbitration algorithms.

one = [
  #           src  dest opaq  payload
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
]

rotate0 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   0,   0x10, 0x10101010 ),
  NetMsgType( 2,   1,   0x11, 0x11111111 ),
  NetMsgType( 0,   2,   0x12, 0x12121212 ),
  NetMsgType( 0,   3,   0x13, 0x13131313 ),
]

rotate1 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   3,   0x13, 0x13131313 ),
  NetMsgType( 2,   0,   0x10, 0x10101010 ),
  NetMsgType( 0,   1,   0x11, 0x11111111 ),
  NetMsgType( 0,   2,   0x12, 0x12121212 ),
]

rotate2 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   2,   0x12, 0x12121212 ),
  NetMsgType( 2,   3,   0x13, 0x13131313 ),
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
  NetMsgType( 0,   1,   0x11, 0x11111111 ),
]

rotate3 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   1,   0x11, 0x11111111 ),
  NetMsgType( 2,   2,   0x12, 0x12121212 ),
  NetMsgType( 0,   3,   0x13, 0x13131313 ),
  NetMsgType( 0,   0,   0x10, 0x10101010 ),
]

all_to_dest0 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   0,   0x10, 0x10101010 ),
  NetMsgType( 2,   0,   0x11, 0x11111111 ),
  NetMsgType( 0,   0,   0x12, 0x12121212 ),
]

all_to_dest1 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   1,   0x10, 0x10101010 ),
  NetMsgType( 2,   1,   0x11, 0x11111111 ),
  NetMsgType( 0,   1,   0x12, 0x12121212 ),
]

all_to_dest2 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   2,   0x10, 0x10101010 ),
  NetMsgType( 2,   2,   0x11, 0x11111111 ),
  NetMsgType( 0,   2,   0x12, 0x12121212 ),
]

all_to_dest3 = [
  #           src  dest opaq  payload
  NetMsgType( 1,   3,   0x10, 0x10101010 ),
  NetMsgType( 2,   3,   0x11, 0x11111111 ),
  NetMsgType( 0,   3,   0x12, 0x12121212 ),
]

#''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Change above tests if necessary; add more directed and random tests
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


#-------------------------------------------------------------------------
# Test Cases: Stream to One Destination
#-------------------------------------------------------------------------

stream_to_dest0 = []
for i in range(16):
  msg = NetMsgType( src=0, dest=0, opaque=i, payload=i )
  stream_to_dest0.append( msg )

stream_to_dest1 = []
for i in range(16):
  msg = NetMsgType( src=0, dest=1, opaque=i, payload=i )
  stream_to_dest1.append( msg )

stream_to_dest2 = []
for i in range(16):
  msg = NetMsgType( src=0, dest=2, opaque=i, payload=i )
  stream_to_dest2.append( msg )

stream_to_dest3 = []
for i in range(16):
  msg = NetMsgType( src=0, dest=3, opaque=i, payload=i )
  stream_to_dest3.append( msg )

#-------------------------------------------------------------------------
# Test Cases: Stream All to Each Destination
#-------------------------------------------------------------------------

stream_all_to_dest0 = []

for i in range(16):
  msg = NetMsgType( src=1, dest=0, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest0.append(msg)

for i in range(16):
  msg = NetMsgType( src=2, dest=0, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest0.append(msg)

for i in range(16):
  msg = NetMsgType( src=0, dest=0, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest0.append(msg)

stream_all_to_dest1 = []

for i in range(16):
  msg = NetMsgType( src=1, dest=1, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest1.append(msg)

for i in range(16):
  msg = NetMsgType( src=2, dest=1, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest1.append(msg)

for i in range(16):
  msg = NetMsgType( src=0, dest=1, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest1.append(msg)

stream_all_to_dest2 = []

for i in range(16):
  msg = NetMsgType( src=1, dest=2, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest2.append(msg)

for i in range(16):
  msg = NetMsgType( src=2, dest=2, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest2.append(msg)

for i in range(16):
  msg = NetMsgType( src=0, dest=2, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest2.append(msg)

stream_all_to_dest3 = []

for i in range(16):
  msg = NetMsgType( src=1, dest=3, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest3.append(msg)

for i in range(16):
  msg = NetMsgType( src=2, dest=3, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest3.append(msg)
  
for i in range(16):
  msg = NetMsgType( src=0, dest=3, opaque=0x00+i, payload=0x0000+i )
  stream_all_to_dest3.append(msg)


#-------------------------------------------------------------------------
# Test Cases: Stream All to All Ports
#-------------------------------------------------------------------------

stream_all_to_all = []
stream_all_to_all.extend( stream_all_to_dest0 )
stream_all_to_all.extend( stream_all_to_dest1 )
stream_all_to_all.extend( stream_all_to_dest2 )
stream_all_to_all.extend( stream_all_to_dest3 )


#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                                  "msgs    src_delay sink_delay delay_mode ordered"),
  [ "one",                            one,                 0,  0,  'fixed',   True  ],
  [ "rotate0",                        rotate0,             0,  0,  'fixed',   True  ],
  [ "rotate1",                        rotate1,             0,  0,  'fixed',   True  ],
  [ "rotate2",                        rotate2,             0,  0,  'fixed',   True  ],
  [ "rotate3",                        rotate3,             0,  0,  'fixed',   True  ],
  [ "all_to_dest0",                   all_to_dest0,        0,  0,  'fixed',   True  ],
  [ "all_to_dest1",                   all_to_dest1,        0,  0,  'fixed',   True  ],
  [ "all_to_dest2",                   all_to_dest2,        0,  0,  'fixed',   True  ],
  [ "all_to_dest3",                   all_to_dest3,        0,  0,  'fixed',   True  ],
  [ "stream_to_dest0",                stream_to_dest0,     0,  0,  'fixed',   True ],
  [ "stream_to_dest1",                stream_to_dest1,     0,  0,  'fixed',   True ],
  [ "stream_to_dest2",                stream_to_dest2,     0,  0,  'fixed',   True ],
  [ "stream_to_dest3",                stream_to_dest3,     0,  0,  'fixed',   True ],
  [ "stream_all_to_dest0",            stream_all_to_dest0, 0,  0,  'fixed',   True ],
  [ "stream_all_to_dest1",            stream_all_to_dest1, 0,  0,  'fixed',   True ],
  [ "stream_all_to_dest2",            stream_all_to_dest2, 0,  0,  'fixed',   True ],
  [ "stream_all_to_dest3",            stream_all_to_dest3, 0,  0,  'fixed',   True ],
  [ "stream_all_to_all",              stream_all_to_all,   0,  0,  'fixed',   True ],

  [ "stream_to_dest0_fixed_2x0",      stream_to_dest0,     2,  0,  'fixed',   True ],
  [ "stream_to_dest1_fixed_2x0",      stream_to_dest1,     2,  0,  'fixed',   True ],
  [ "stream_to_dest2_fixed_2x0",      stream_to_dest2,     2,  0,  'fixed',   True ],
  [ "stream_to_dest3_fixed_2x0",      stream_to_dest3,     2,  0,  'fixed',   True ],

  [ "stream_all_to_dest0_fixed_0x2",  stream_all_to_dest0, 0,  2,  'fixed',   True ],
  [ "stream_all_to_dest1_fixed_0x2",  stream_all_to_dest1, 0,  2,  'fixed',   True ],
  [ "stream_all_to_dest2_fixed_0x2",  stream_all_to_dest2, 0,  2,  'fixed',   True ],
  [ "stream_all_to_dest3_fixed_0x2",  stream_all_to_dest3, 0,  2,  'fixed',   True ],
  [ "stream_all_to_all_fixed_0x2",    stream_all_to_all,   0,  2,  'fixed',   True ],

  [ "stream_all_to_dest0_rand_delay", stream_all_to_dest0, 0, 20,  'random',  True ],
  [ "stream_all_to_dest1_rand_delay", stream_all_to_dest1, 0, 20,  'random',  True ],
  [ "stream_all_to_dest2_rand_delay", stream_all_to_dest2, 0, 20,  'random',  True ],
  [ "stream_all_to_dest3_rand_delay", stream_all_to_dest3, 0, 20,  'random',  True ],
  [ "stream_all_to_all_rand_delay",   stream_all_to_all,   0, 20,  'random',  False ], # too hard to be ordered
])

def sort_by_round_robin(msgs, src_order):
    """
    Sort messages based on Round-Robin order of src.
    :param msgs: List of messages to sort.
    :param src_order: List of src indices in Round-Robin order.
    :return: Sorted list of messages.
    """
    # Create buffers for each src
    src_buffers = {int(src): [] for src in src_order}  # Ensure src_order keys are integers
    for msg in msgs:
        src_buffers[int(msg.src)].append(msg)  # Convert msg.src to int before accessing src_buffers

    # Merge messages based on Round-Robin order
    sorted_msgs = []
    while any(src_buffers.values()):
        for src in src_order:
            if src_buffers[src]:
                sorted_msgs.append(src_buffers[src].pop(0))

    return sorted_msgs
#-------------------------------------------------------------------------
# test w/ router id == 0
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test_router_id_0( test_params, cmdline_opts ):

  th = TestHarness( router_id=0 )
  router_id=0
  th.set_param("top.srcs[0].construct",
    msgs                = [ m for m in test_params.msgs if m.src == 0 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.srcs[1].construct",
    msgs                = [ m for m in test_params.msgs if m.src == 1 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.srcs[2].construct",
    msgs                = [ m for m in test_params.msgs if m.src == 2 ],
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.src_delay,
    interval_delay      = test_params.src_delay )

  th.set_param("top.sinks[0].construct",
    msgs                = sort_by_round_robin(
                            [ m for m in test_params.msgs if (m.dest != router_id and ((m.dest - router_id) & 3) >= ((router_id - m.dest) & 3)) ],
                            src_order=[1, 2, 0]  # Round-Robin priority for src
                          ),    
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay,
    ordered             = test_params.ordered )

  th.set_param("top.sinks[1].construct",
    msgs                = sort_by_round_robin(
                            [ m for m in test_params.msgs if (m.dest != router_id and ((m.dest - router_id) & 3) < ((router_id - m.dest) & 3)) ],
                            src_order=[1, 2, 0]  # Round-Robin priority for src
                          ),    
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay,
    ordered             = test_params.ordered )

  th.set_param("top.sinks[2].construct",
    msgs                = sort_by_round_robin(
                            [ m for m in test_params.msgs if m.dest == router_id ],
                            src_order=[1, 2, 0]  # Round-Robin priority for src
                          ),    
    interval_delay_mode = test_params.delay_mode,
    initial_delay       = test_params.sink_delay,
    interval_delay      = test_params.sink_delay,
    ordered             = test_params.ordered )

  th.elaborate()

  run_sim( th, cmdline_opts, duts=['router'] )

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

