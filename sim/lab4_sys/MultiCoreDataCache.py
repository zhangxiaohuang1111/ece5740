#=========================================================================
# MultiCoreDataCache PyMTL3 Wrapper
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.mem.ifcs import MemRequesterIfc, MemResponderIfc
from pymtl3.stdlib.mem      import mk_mem_msg

class MultiCoreDataCache( VerilogPlaceholder, Component ):
  def construct( s ):

    CacheReqType, CacheRespType = mk_mem_msg( 8, 32, 32  )
    MemReqType,   MemRespType   = mk_mem_msg( 8, 32, 128 )

    s.proc2cache = [ MemResponderIfc( CacheReqType, CacheRespType ) for _ in range(4) ]
    s.cache2mem  = MemRequesterIfc( MemReqType, MemRespType )

