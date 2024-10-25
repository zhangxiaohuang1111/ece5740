#=========================================================================
# simple_test.py
#=========================================================================
# This is primarily just for playing around with little transaction
# sequences.

from pymtl3.stdlib.test_utils import run_sim

from lab3_mem.test.harness    import req, resp, TestHarness
from lab3_mem.CacheFL         import CacheFL
from lab3_mem.CacheBase       import CacheBase
from lab3_mem.CacheAlt        import CacheAlt

#----------------------------------------------------------------------
# test
#----------------------------------------------------------------------

def test( cmdline_opts ):

  msgs = [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in',  0x0, 0,   0,  0          ),
  ]

  th = TestHarness( CacheFL() )

  th.set_param("top.src.construct",  msgs=msgs[::2]  )
  th.set_param("top.sink.construct", msgs=msgs[1::2] )

  run_sim( th, cmdline_opts, duts=['cache'] )

