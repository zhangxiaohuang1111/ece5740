#=========================================================================
# CacheFL_test.py
#=========================================================================

import pytest

from random import seed, randint, choice

from pymtl3 import *
from pymtl3.stdlib.mem        import MemMsgType
from pymtl3.stdlib.test_utils import mk_test_case_table

from lab3_mem.test.harness import req, resp, run_test
from lab3_mem.CacheFL      import CacheFL

seed(0xa4e28cc2)

#-------------------------------------------------------------------------
# cmp_wo_test_field
#-------------------------------------------------------------------------
# The test field in the cache response is used to indicate if the
# corresponding memory access resulted in a hit or a miss. However, the
# FL model always sets the test field to zero since it does not track
# hits/misses. So we need to do something special to ignore the test
# field when using the FL model. To do this, we can pass in a specialized
# comparison function to the StreamSinkFL.

def cmp_wo_test_field( msg, ref ):

  if msg.type_ != ref.type_:
    return False

  if msg.len != ref.len:
    return False

  if msg.opaque != msg.opaque:
    return False

  if ref.data != msg.data:
    return False

  # do not check the test field

  return True

#-------------------------------------------------------------------------
# Data
#-------------------------------------------------------------------------
# These functions are used to specify the address/data to preload into
# the main memory before running a test.

# 64B of sequential data

def data_64B():
  return [
    # addr      data
    0x00001000, 0x000c0ffe,
    0x00001004, 0x10101010,
    0x00001008, 0x20202020,
    0x0000100c, 0x30303030,
    0x00001010, 0x40404040,
    0x00001014, 0x50505050,
    0x00001018, 0x60606060,
    0x0000101c, 0x70707070,
    0x00001020, 0x80808080,
    0x00001024, 0x90909090,
    0x00001028, 0xa0a0a0a0,
    0x0000102c, 0xb0b0b0b0,
    0x00001030, 0xc0c0c0c0,
    0x00001034, 0xd0d0d0d0,
    0x00001038, 0xe0e0e0e0,
    0x0000103c, 0xf0f0f0f0,
  ]

# 512B of sequential data

def data_512B():
  data = []
  for i in range(128):
    data.extend([0x00001000+i*4,0xabcd1000+i*4])
  return data

# 1024B of random data

def data_random():
  seed(0xdeadbeef)
  data = []
  for i in range(256):
    data.extend([0x00001000+i*4,randint(0,0xffffffff)])
  return data

#----------------------------------------------------------------------
# Test Cases for Write Init
#----------------------------------------------------------------------

# Just make sure a single write init goes through the memory system.

def write_init_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),
  ]

# Write init a word multiple times, also tests opaque bits

def write_init_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x3, 0,   0,  0    ),
  ]

# Use write inits for each word in a cache line

def write_init_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1004, 0, 0x02020202 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1008, 0, 0x03030303 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x100c, 0, 0x04040404 ), resp( 'in', 0x3, 0,   0,  0    ),
  ]

# Write init one word in each cacheline in half the cache. For the direct
# mapped cache, this will write the first half of all the sets. For the
# set associative cache, this will write all of the sets in the first
# way.

def write_init_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0    ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0    ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0    ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0    ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0    ),
  ]

#----------------------------------------------------------------------
# Test Cases for Read Hits
#----------------------------------------------------------------------

# Single read hit

def read_hit_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xdeadbeef ),
  ]

# Read same word multiple times, also tests opaque bits

def read_hit_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xdeadbeef ),
  ]

# Read every word in cache line

def read_hit_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1004, 0, 0x02020202 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1008, 0, 0x03030303 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x100c, 0, 0x04040404 ), resp( 'in', 0x3, 0,   0,  0    ),

    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x01010101 ),
    req( 'rd', 0x5, 0x1004, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x02020202 ),
    req( 'rd', 0x6, 0x1008, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'rd', 0x7, 0x100c, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x04040404 ),
  ]

# Read one word from each cacheline

def read_hit_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x00000000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x02020202 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x03030303 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x04040404 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x05050505 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x06060606 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x07070707 ),
  ]

#----------------------------------------------------------------------
# Test Cases for Write Hits
#----------------------------------------------------------------------

# Single write hit to one word

def write_hit_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
  ]

# Write/read word multiple times, also tests opaque bits

def write_hit_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'wr', 0x3, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'wr', 0x5, 0x1000, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'rd', 0x6, 0x1000, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'wr', 0x7, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read every word in cache line

def write_hit_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x1004, 0, 0x02020202 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x1008, 0, 0x03030303 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x100c, 0, 0x04040404 ), resp( 'in', 0x0, 0,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x5, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x7, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'rd', 0x4, 0x1004, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'rd', 0x6, 0x1008, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'rd', 0x8, 0x100c, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read one word from each cacheline

def write_hit_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, 0x10101010 ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x12121212 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x13131313 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x15151515 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x16161616 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x17171717 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
  ]

#----------------------------------------------------------------------
# Test Cases for Refill on Read Miss
#----------------------------------------------------------------------

# Single read miss (uses data_64B)

def read_miss_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x000c0ffe ),
  ]

# Read same word multiple times, also tests opaque bits (uses data_64B)

def read_miss_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x000c0ffe ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x000c0ffe ),
  ]

# Read every word in cache line (uses data_64B)

def read_miss_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x000c0ffe ),
    req( 'rd', 0x2, 0x1004, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x10101010 ),
    req( 'rd', 0x3, 0x1008, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x20202020 ),
    req( 'rd', 0x4, 0x100c, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x30303030 ),
  ]

# Read miss for each cacheline, then read hit for each cacheline (uses data_512B)

def read_miss_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1010 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1020 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1030 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1040 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1050 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1060 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1070 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1080 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1090 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd10a0 ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd10b0 ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd10c0 ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd10d0 ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd10e0 ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd10f0 ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1010 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1020 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1030 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1040 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1050 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1060 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1070 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1080 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1090 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd10a0 ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd10b0 ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd10c0 ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd10d0 ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd10e0 ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd10f0 ),

    req( 'rd', 0x0, 0x1004, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1004 ),
    req( 'rd', 0x1, 0x1014, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1014 ),
    req( 'rd', 0x2, 0x1024, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1024 ),
    req( 'rd', 0x3, 0x1034, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1034 ),
    req( 'rd', 0x4, 0x1044, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1044 ),
    req( 'rd', 0x5, 0x1054, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1054 ),
    req( 'rd', 0x6, 0x1064, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1064 ),
    req( 'rd', 0x7, 0x1074, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1074 ),
    req( 'rd', 0x8, 0x1084, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1084 ),
    req( 'rd', 0x9, 0x1094, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1094 ),
    req( 'rd', 0xa, 0x10a4, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd10a4 ),
    req( 'rd', 0xb, 0x10b4, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd10b4 ),
    req( 'rd', 0xc, 0x10c4, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd10c4 ),
    req( 'rd', 0xd, 0x10d4, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd10d4 ),
    req( 'rd', 0xe, 0x10e4, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd10e4 ),
    req( 'rd', 0xf, 0x10f4, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd10f4 ),
  ]

#----------------------------------------------------------------------
# Test Cases for Refill on Write Miss
#----------------------------------------------------------------------

# Single write miss to one word (uses data_64B)

def write_miss_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
  ]

# Write/read word multiple times, also tests opaque bits (uses data_64B)

def write_miss_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'wr', 0x3, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'wr', 0x5, 0x1000, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'rd', 0x6, 0x1000, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'wr', 0x7, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read every word in cache line (uses data_64B)

def write_miss_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x4, 1,   0,  0          ),

    req( 'rd', 0x5, 0x1000, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x01010101 ),
    req( 'rd', 0x6, 0x1004, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x02020202 ),
    req( 'rd', 0x7, 0x1008, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x03030303 ),
    req( 'rd', 0x8, 0x100c, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read one word from each cacheline (uses data_512B)

def write_miss_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1020, 0, 0x12121212 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1030, 0, 0x13131313 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1040, 0, 0x14141414 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1050, 0, 0x15151515 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1060, 0, 0x16161616 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1070, 0, 0x17171717 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x1080, 0, 0x18181818 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x1090, 0, 0x19191919 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0x10a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0x10b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0x10c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0x10d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0x10e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0x10f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),
  ]

#----------------------------------------------------------------------
# Test Cases for Evict
#----------------------------------------------------------------------

# Write miss to two cachelines, and then a read to a third cacheline.
# This read to the third cacheline is guaranteed to cause an eviction on
# both the direct mapped and set associative caches. (uses data_512B)

def evict_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
    req( 'wr', 0x0, 0x1080, 0, 0x000c0ffe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1080, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xcafecafe ),
  ]

# Write word and evict multiple times. Test is carefully crafted to
# ensure it applies to both direct mapped and set associative caches.
# (uses data_512B)

def evict_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'wr', 0x2, 0x1080, 0, 0x11111111 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'rd', 0x3, 0x1080, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x11111111 ),
    req( 'rd', 0x4, 0x1100, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x5, 0x1080, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x11111111 ), # make sure way1 is still LRU

    req( 'wr', 0x6, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'rd', 0x7, 0x1000, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x02020202 ),
    req( 'wr', 0x8, 0x1080, 0, 0x12121212 ), resp( 'wr', 0x8, 1,   0,  0          ),
    req( 'rd', 0x9, 0x1080, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x12121212 ),
    req( 'rd', 0xa, 0x1100, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0xb, 0x1080, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x12121212 ), # make sure way1 is still LRU

    req( 'wr', 0xc, 0x1000, 0, 0x03030303 ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'rd', 0xd, 0x1000, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x03030303 ),
    req( 'wr', 0xe, 0x1080, 0, 0x13131313 ), resp( 'wr', 0xe, 1,   0,  0          ),
    req( 'rd', 0xf, 0x1080, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x13131313 ),
    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x1, 0x1080, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x13131313 ), # make sure way1 is still LRU

    req( 'wr', 0x2, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x04040404 ),
    req( 'wr', 0x4, 0x1080, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'rd', 0x5, 0x1080, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x14141414 ),
    req( 'rd', 0x6, 0x1100, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x7, 0x1080, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x14141414 ), # make sure way1 is still LRU

    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x04040404 ),
  ]

# Write every word on two cachelines, and then a read to a third
# cacheline. This read to the third cacheline is guaranteed to cause an
# eviction on both the direct mapped and set associative caches. (uses
# data_512B)

def evict_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x3, 1,   0,  0          ),

    req( 'wr', 0x4, 0x1080, 0, 0x11111111 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1084, 0, 0x12121212 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x1088, 0, 0x13131313 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x108c, 0, 0x14141414 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x8, 0x1100, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1100 ), # conflicts

    req( 'rd', 0x9, 0x1000, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x01010101 ),
    req( 'rd', 0xa, 0x1004, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x02020202 ),
    req( 'rd', 0xb, 0x1008, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x03030303 ),
    req( 'rd', 0xc, 0x100c, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x04040404 ),
  ]

# Write one word from each cacheline, then evict (uses data_512B)

def evict_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1020, 0, 0x12121212 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1030, 0, 0x13131313 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1040, 0, 0x14141414 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1050, 0, 0x15151515 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1060, 0, 0x16161616 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1070, 0, 0x17171717 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x1080, 0, 0x18181818 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x1090, 0, 0x19191919 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0x10a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0x10b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0x10c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0x10d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0x10e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0x10f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),

    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x1, 0x1110, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1110 ), # conflicts
    req( 'rd', 0x2, 0x1120, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1120 ), # conflicts
    req( 'rd', 0x3, 0x1130, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1130 ), # conflicts
    req( 'rd', 0x4, 0x1140, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1140 ), # conflicts
    req( 'rd', 0x5, 0x1150, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1150 ), # conflicts
    req( 'rd', 0x6, 0x1160, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1160 ), # conflicts
    req( 'rd', 0x7, 0x1170, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1170 ), # conflicts
    req( 'rd', 0x8, 0x1180, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1180 ), # conflicts
    req( 'rd', 0x9, 0x1190, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1190 ), # conflicts
    req( 'rd', 0xa, 0x11a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd11a0 ), # conflicts
    req( 'rd', 0xb, 0x11b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd11b0 ), # conflicts
    req( 'rd', 0xc, 0x11c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd11c0 ), # conflicts
    req( 'rd', 0xd, 0x11d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd11d0 ), # conflicts
    req( 'rd', 0xe, 0x11e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd11e0 ), # conflicts
    req( 'rd', 0xf, 0x11f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd11f0 ), # conflicts

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0x1f1f1f1f ),
  ]


# Read hit path for clean lines
def read_hit_clean_line():
    return [
        # type  opq   addr          len   data                 type  opq   test    len    data
        req('in', 0x0, 0x1000, len=0, data=0x12345678), resp('in', 0x0, test=0, len=0, data=0),  # Initialize line
        req('rd', 0x1, 0x1000, len=0, data=0),          resp('rd', 0x1, test=1, len=0, data=0x12345678)  # Read clean line
    ]

# Write hit path for clean lines
def write_hit_clean_line():
    return [
        # type  opq   addr          len   data                 type  opq   test    len    data
        req('in', 0x0, 0x1000, len=0, data=0x12345678), resp('in', 0x0, test=0, len=0, data=0),  # Initialize line
        req('wr', 0x1, 0x1000, len=0, data=0xabcdef00), resp('wr', 0x1, test=1, len=0, data=0)   # Write clean line
    ]

# Read hit path for dirty lines
def read_hit_dirty_line():
    return [
        # type  opq   addr          len   data                 type  opq   test    len    data
        req('wr', 0x0, 0x1000, len=0, data=0xdeadbeef), resp('wr', 0x0, test=0, len=0, data=0),  # Write to make line dirty
        req('rd', 0x1, 0x1000, len=0, data=0),          resp('rd', 0x1, test=1, len=0, data=0xdeadbeef)  # Read dirty line
    ]

# Write hit path for dirty lines
def write_hit_dirty_line():
    return [
        # type  opq   addr          len   data                 type  opq   test    len    data
        req('wr', 0x0, 0x1000, len=0, data=0xdeadbeef), resp('wr', 0x0, test=0, len=0, data=0),  # Initial write to make dirty
        req('wr', 0x1, 0x1000, len=0, data=0xcafebabe), resp('wr', 0x1, test=1, len=0, data=0)   # Write hit to update dirty line
    ]

# Read miss with refill and no eviction
def read_miss_refill_no_evict():
    return [
        # type  opq   addr          len   data                 type  opq   test    len    data
        req('rd', 0x0, 0x1000, len=0, data=0),          resp('rd', 0x0, test=0, len=0, data=0x000c0ffe),  # Miss and refill
        req('rd', 0x1, 0x1004, len=0, data=0),          resp('rd', 0x1, test=1, len=0, data=0x10101010)   # Read hit after refill
    ]

# Write miss with refill and no eviction
def write_miss_refill_no_evict():
    return [
        # type  opq   addr          len   data                 type  opq   test    len    data
        req('wr', 0x0, 0x1000, len=0, data=0x87654321), resp('wr', 0x0, test=0, len=0, data=0),  # Miss and refill
        req('rd', 0x1, 0x1000, len=0, data=0),          resp('rd', 0x1, test=1, len=0, data=0x87654321),   # Read hit after refill
        req('rd', 0x1, 0x1004, len=0, data=0),          resp('rd', 0x1, test=1, len=0, data=0x10101010)   # Read hit after refill
    ]

# Read miss with refill and eviction
def read_miss_refill_evict():
      return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
    req( 'wr', 0x0, 0x1080, 0, 0x000c0ffe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1080, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xcafecafe ),
  ]

# Write miss with refill and eviction
def write_miss_refill_evict():
    return [
        #    type  opq  addr   len data                type  opq  test len data
        req('wr', 0x0, 0x1000, 0, 0xdeadbeef), resp('wr', 0x0, 0,   0,  0          ),  # Write to address 0x1000
        req('rd', 0x0, 0x1000, 0, 0          ),resp('rd', 0x0, 1,   0,  0xdeadbeef ),  # Read to verify write
        req('wr', 0x0, 0x1080, 0, 0x12345678), resp('wr', 0x0, 0,   0,  0          ),  # Write to a different address (fills cache)
        req('rd', 0x0, 0x1080, 0, 0          ),resp('rd', 0x0, 1,   0,  0x12345678 ),  # Read to verify write
        req('wr', 0x0, 0x1100, 0, 0xcafecafe), resp('wr', 0x0, 0,   0,  0          ),  # Write causing conflict, triggers eviction
        req('rd', 0x0, 0x1000, 0, 0          ),resp('rd', 0x0, 0,   0,  0xdeadbeef ),  # Refill from main memory after eviction
    ]

def capacity_miss_test():
    return [
        #    type  opq  addr      len data             type  opq  test len data
        req('wr', 0x0, 0x00001000, 0, 777),       resp('wr', 0x0,   0,  0,  0), 
        req('wr', 0x1, 0x00001010, 0, 1),         resp('wr', 0x1,   0,  0,  0), 
        req('wr', 0x2, 0x00001020, 0, 2),         resp('wr', 0x2,   0,  0,  0), 
        req('wr', 0x3, 0x00001030, 0, 3),         resp('wr', 0x3,   0,  0,  0), 
        req('wr', 0x4, 0x00001040, 0, 4),         resp('wr', 0x4,   0,  0,  0), 
        req('wr', 0x5, 0x00001050, 0, 5),         resp('wr', 0x5,   0,  0,  0), 
        req('wr', 0x6, 0x00001060, 0, 6),         resp('wr', 0x6,   0,  0,  0), 
        req('wr', 0x7, 0x00001070, 0, 7),         resp('wr', 0x7,   0,  0,  0), 
        req('wr', 0x8, 0x00001080, 0, 8),         resp('wr', 0x8,   0,  0,  0),
        req('wr', 0x9, 0x00001090, 0, 9),         resp('wr', 0x9,   0,  0,  0),
        req('wr', 0xa, 0x000010a0, 0, 10),        resp('wr', 0xa,   0,  0,  0),
        req('wr', 0xb, 0x000010b0, 0, 11),        resp('wr', 0xb,   0,  0,  0),
        req('wr', 0xc, 0x000010c0, 0, 12),        resp('wr', 0xc,   0,  0,  0),
        req('wr', 0xd, 0x000010d0, 0, 13),        resp('wr', 0xd,   0,  0,  0),
        req('wr', 0xe, 0x000010e0, 0, 14),        resp('wr', 0xe,   0,  0,  0),
        req('wr', 0xf, 0x000010f0, 0, 15),        resp('wr', 0xf,   0,  0,  0),
        req('wr', 0x10,0x00001100, 0, 16),        resp('wr', 0x10,  0,  0,  0), # capacity miss
        req('rd', 0x11,0x00001100, 0, 0),         resp('rd', 0x11,  1,  0, 16), # read
        req('rd', 0x11,0x00001000, 0, 0),         resp('rd', 0x11,  0,  0,777), # capacity miss, but get from main memory
    

    ]

#-------------------------------------------------------------------------
# Generic tests
#-------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                                    "msg_func                    mem_data_func stall lat src sink"),

  [ "write_init_word",                  write_init_word,            None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_word",            write_init_multi_word,      None,         0.0,  0,  0,  0    ],
  [ "write_init_cacheline",             write_init_cacheline,       None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_cacheline",       write_init_multi_cacheline, None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_word_sink_delay", write_init_multi_word,      None,         0.0,  0,  0,  10   ],
  [ "write_init_multi_word_src_delay",  write_init_multi_word,      None,         0.0,  0,  10, 0    ],

  [ "read_hit_word",                    read_hit_word,              None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_word",              read_hit_multi_word,        None,         0.0,  0,  0,  0    ],
  [ "read_hit_cacheline",               read_hit_cacheline,         None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_cacheline",         read_hit_multi_cacheline,   None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_word_sink_delay",   read_hit_multi_word,        None,         0.0,  0,  0,  10   ],
  [ "read_hit_multi_word_src_delay",    read_hit_multi_word,        None,         0.0,  0,  10, 0    ],

  [ "write_hit_word",                   write_hit_word,             None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word",             write_hit_multi_word,       None,         0.0,  0,  0,  0    ],
  [ "write_hit_cacheline",              write_hit_cacheline,        None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_cacheline",        write_hit_multi_cacheline,  None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word_sink_delay",  write_hit_multi_word,       None,         0.0,  0,  0,  10   ],
  [ "write_hit_multi_word_src_delay",   write_hit_multi_word,       None,         0.0,  0,  10, 0    ],

  [ "read_miss_word",                   read_miss_word,             data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_word",             read_miss_multi_word,       data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_cacheline",              read_miss_cacheline,        data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_cacheline",        read_miss_multi_cacheline,  data_512B,    0.0,  0,  0,  0    ],
  [ "read_miss_multi_word_sink_delay",  read_miss_multi_word,       data_64B,     0.9,  3,  0,  10   ],
  [ "read_miss_multi_word_src_delay",   read_miss_multi_word,       data_64B,     0.9,  3,  10, 0    ],

  [ "write_miss_word",                  write_miss_word,            data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_word",            write_miss_multi_word,      data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_cacheline",             write_miss_cacheline,       data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_cacheline",       write_miss_multi_cacheline, data_512B,    0.0,  0,  0,  0    ],
  [ "write_miss_multi_word_sink_delay", write_miss_multi_word,      data_64B,     0.9,  3,  0,  10   ],
  [ "write_miss_multi_word_src_delay",  write_miss_multi_word,      data_64B,     0.9,  3,  10, 0    ],

  [ "evict_word",                       evict_word,                 data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_word",                 evict_multi_word,           data_512B,    0.0,  0,  0,  0    ],
  [ "evict_cacheline",                  evict_cacheline,            data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_cacheline",            evict_multi_cacheline,      data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_word_sink_delay",      evict_multi_word,           data_512B,    0.9,  3,  0,  10   ],
  [ "evict_multi_word_src_delay",       evict_multi_word,           data_512B,    0.9,  3,  10, 0    ],

  # more tests for lab3
  [ "read_hit_clean_line",              read_hit_clean_line,        None,         0.0,  0,  0,  0    ],
  [ "write_hit_clean_line",             write_hit_clean_line,       None,         0.0,  0,  0,  0    ],
  [ "read_hit_dirty_line",              read_hit_dirty_line,        None,         0.0,  0,  0,  0    ],
  [ "write_hit_dirty_line",             write_hit_dirty_line,       None,         0.0,  0,  0,  0    ],
  [ "read_miss_refill_no_evict",        read_miss_refill_no_evict,  data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_refill_no_evict",       write_miss_refill_no_evict, data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_refill_evict",           read_miss_refill_evict,     data_512B,    0.0,  0,  0,  0    ],
  [ "write_miss_refill_evict",          write_miss_refill_evict,    data_512B,    0.0,  0,  0,  0    ],
  [ "capacity_miss_test",               capacity_miss_test,         data_64B,     0.0,  0,  0,  0    ],
])

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Case with Random Addresses and Data
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# Random test messages
#-------------------------------------------------------------------------

def simple_pattern_single_req_random_msgs():
  # 
  msgs = []
  for i in range(100):
    # 
    idx = randint(0, 255)  #
    addr = 0x00001000 + idx * 4
    data = data_random()[2 * idx + 1]  # 

    # 
    msgs.extend([
      req('rd', i, addr, 0, 0), resp('rd', i, 1, 0, data),
    ])

  return msgs

def random_write_read_msgs():
    msgs = []
    for i in range(256):
        # 
        idx = randint(0, 255)
        addr = 0x00001000 + idx * 4
        data = 0x1000 + idx  #  data_random
        
        # 
        msgs.extend([
            req('wr', i, addr, 0, data), resp('wr', i, 0, 0, 0),   # 
            req('rd', i, addr, 0, 0),    resp('rd', i, 1, 0, data),   # 
        ])

    return msgs

def stress_test():
    msgs = []
    num_lines = 16  # Number of cache lines
    line_size = 16  # Size of each cache line in bytes
    base_addr = 0x00001000  # Starting address for initial fill
    new_base_addr = 0x00002000  # Address range for eviction phase
    max_opq = num_lines * 4  # Maximum opaque value to differentiate stages

    # --- Step 1: Initial cache fill ---
    for i in range(num_lines):
        addr_base = base_addr + i * line_size
        data_list = [i * 4 + j for j in range(4)]  # Deterministic data for each word
        for j in range(4):
            addr = addr_base + j * 4
            data = data_list[j]
            opq = i * 4 + j
            # Initial write to fill cache line; first write is treated as a miss
            msgs.extend([
                req('wr', opq, addr, 0, data), resp('wr', opq, 0 if j == 0 else 1, 0, 0)
            ])
        for j in range(4):
            addr = addr_base + j * 4
            msgs.extend([
                req('rd', i * 4 + j, addr, 0, 0), resp('rd', i * 4 + j, 1, 0, data_list[j])
            ])

    # --- Step 2: Evict cache by writing to new addresses ---
    for i in range(num_lines):
        addr_base = new_base_addr + i * line_size
        data_list = [100 + i * 4 + j for j in range(4)]  # Deterministic data for eviction phase
        for j in range(4):
            addr = addr_base + j * 4
            data = data_list[j]
            opq = max_opq + i * 4 + j
            # New addresses cause evictions; first write in each line is treated as a miss
            msgs.extend([
                req('wr', opq, addr, 0, data), resp('wr', opq, 0 if j == 0 else 1, 0, 0)
            ])
        for j in range(4):
            addr = addr_base + j * 4
            msgs.extend([
                req('rd', max_opq + i * 4 + j, addr, 0, 0), resp('rd', max_opq + i * 4 + j, 1, 0, data_list[j])
            ])

    # --- Step 3: Re-access initial addresses to validate eviction ---
    for i in range(num_lines):
        addr_base = base_addr + i * line_size
        data_list = [i * 4 + j for j in range(4)]  # Reuse initial data for validation
        for j in range(4):
            addr = addr_base + j * 4
            data = data_list[j]
            opq = max_opq * 2 + i * 4 + j
            # The first re-accessed address should miss, with subsequent hits
            msgs.extend([
                req('wr', opq, addr, 0, data), resp('wr', opq, 0 if j == 0 else 1, 0, 0)
            ])
        for j in range(4):
            addr = addr_base + j * 4
            msgs.extend([
                req('rd', max_opq * 2 + i * 4 + j, addr, 0, 0), resp('rd', max_opq * 2 + i * 4 + j, 1, 0, data_list[j])
            ])
    return msgs

def random_stress_test():
    msgs = []
    num_lines = 16  # Number of cache lines
    line_size = 16  # Size of each cache line in bytes
    base_addr = 0x00001000  # Starting address for initial fill
    new_base_addr = 0x00002000  # Address range for eviction phase
    max_opq = num_lines * 4  # Maximum opaque value to differentiate stages

    # --- Step 1: Initial cache fill ---
    for i in range(num_lines):
        addr_base = base_addr + i * line_size
        data_list = [randint(0, 0xffffffff) for _ in range(4)]
        for j in range(4):
            addr = addr_base + j * 4
            data = data_list[j]
            opq = i * 4 + j
            msgs.extend([
                req('wr', opq, addr, 0, data), resp('wr', opq, 0 if j == 0 else 1, 0, 0)
            ])
        for j in range(4):
            addr = addr_base + j * 4
            msgs.extend([
                req('rd', i * 4 + j, addr, 0, 0), resp('rd', i * 4 + j, 1, 0, data_list[j])
            ])

    # --- Step 2: Evict cache by writing to new addresses ---
    for i in range(num_lines):
        addr_base = new_base_addr + i * line_size
        data_list = [randint(0, 0xffffffff) for _ in range(4)]
        for j in range(4):
            addr = addr_base + j * 4
            data = data_list[j]
            opq = max_opq + i * 4 + j
            msgs.extend([
                req('wr', opq, addr, 0, data), resp('wr', opq, 0 if j == 0 else 1, 0, 0)
            ])
        for j in range(4):
            addr = addr_base + j * 4
            msgs.extend([
                req('rd', max_opq + i * 4 + j, addr, 0, 0), resp('rd', max_opq + i * 4 + j, 1, 0, data_list[j])
            ])

    # --- Step 3: Re-access initial addresses to validate eviction ---
    for i in range(num_lines):
        addr_base = base_addr + i * line_size
        data_list = [randint(0, 0xffffffff) for _ in range(4)]
        for j in range(4):
            addr = addr_base + j * 4
            data = data_list[j]
            opq = max_opq * 2 + i * 4 + j
            msgs.extend([
                req('wr', opq, addr, 0, data), resp('wr', opq, 0 if j == 0 else 1, 0, 0)
            ])
        for j in range(4):
            addr = addr_base + j * 4
            msgs.extend([
                req('rd', max_opq * 2 + i * 4 + j, addr, 0, 0), resp('rd', max_opq * 2 + i * 4 + j, 1, 0, data_list[j])
            ])

    return msgs

def simple_pattern_random_req_data_msg():
    # Initialize address-data map with data_random contents
    seed(0xdeadbeef)  # Ensure the same seed as data_random()
    addr_data_map = {}
    base_addr = 0x00001000
    data_random_list = data_random()
    for i in range(0, len(data_random_list), 2):
        addr = data_random_list[i]
        data = data_random_list[i+1]
        addr_data_map[addr] = data

    # Now create the test messages
    msgs = []
    # Let's perform 16 operations, randomly choosing between write and read
    for i in range(16):
        addr = base_addr + randint(0, 255) * 4  # Random address in the range
        req_type = 'wr' if randint(0,1) == 0 else 'rd'  # Randomly choose to read or write

        if req_type == 'wr':
            # Generate random data for write
            data = randint(0, 0xffffffff)
            addr_data_map[addr] = data  # Update the data map with new data
            msgs.extend([
                req('wr', i, addr, 0, data),  # Write request
                resp('wr', i, 0, 0, 0),       # Expected write response
            ])
        else:
            # For read requests, get expected data from addr_data_map
            expected_data = addr_data_map.get(addr, 0)
            hit = 1 if addr in addr_data_map else 0  # Determine if it's a hit or miss
            msgs.extend([
                req('rd', i, addr, 0, 0),           # Read request
                resp('rd', i, hit, 0, expected_data),  # Expected read response
            ])

    return msgs

def random_pattern_random_req_data_msg():
    # Initialize the random seed for reproducibility
    seed(0xdeadbeef)
    
    # Initialize the address-data map with the initial memory contents
    addr_data_map = {}
    base_addr = 0x00001000
    data_random_list = data_random()  # Assume this function returns a list like [addr1, data1, addr2, data2, ...]
    for i in range(0, len(data_random_list), 2):
        addr = data_random_list[i]
        data = data_random_list[i+1]
        addr_data_map[addr] = data
    
    # Generate a list of test messages
    msgs = []
    num_operations = 100  # Total number of cache operations to perform
    
    for i in range(num_operations):
        # Generate a random address within a specified range
        addr = base_addr + randint(0, 255) * 4  # Addresses are word-aligned
        
        # Randomly choose to perform a read or write
        req_type = 'wr' if randint(0, 1) == 0 else 'rd'
        
        if req_type == 'wr':
            # For write requests, generate random data
            data = randint(0, 0xffffffff)
            # Update the address-data map with the new data
            addr_data_map[addr] = data
            # Append the write request and expected response
            msgs.extend([
                req('wr', i, addr, 0, data),  # Write request
                resp('wr', i, 0, 0, 0),       # Expected write response (FL model always sets test field to 0)
            ])
        else:
            # For read requests, get the expected data from the address-data map
            expected_data = addr_data_map.get(addr, 0)
            # Append the read request and expected response
            msgs.extend([
                req('rd', i, addr, 0, 0),           # Read request
                resp('rd', i, 1, 0, expected_data),  # Expected read response (FL model always sets test field to 1 for hits)
            ])
    
    return msgs

def unit_stride_random_data_msgs():
    # Initialize the random seed for reproducibility
    seed(0xdeadbeef)
    
    # Initialize the address-data map to keep track of written data
    addr_data_map = {}
    base_addr = 0x00001000  # Starting address for unit stride access
    num_accesses = 64       # Number of accesses to perform

    # Build initial memory map
    data_random_list = data_random()
    initial_mem_map = {}
    for i in range(0, len(data_random_list), 2):
        addr = data_random_list[i]
        data = data_random_list[i+1]
        initial_mem_map[addr] = data

    # Generate the test messages
    msgs = []
    for i in range(num_accesses):
        addr = base_addr + i * 4  # Sequential addresses with word (4-byte) stride
        req_type = 'wr' if i % 2 == 0 else 'rd'  # Alternate between write and read
        
        if req_type == 'wr':
            # Generate random data for write operations
            data = randint(0, 0xffffffff)
            addr_data_map[addr] = data  # Update the data map with the new data
            # Append the write request and expected response to the message list
            msgs.extend([
                req('wr', i, addr, 0, data),  # Write request
                resp('wr', i, 0, 0, 0),       # Expected write response (test field is 0)
            ])
        else:
            # For read operations
            if addr in addr_data_map:
                # If address has been written before, expect a hit
                expected_data = addr_data_map[addr]
                test_field = 1  # Hit
            else:
                # If address hasn't been written before, expect a miss
                expected_data = initial_mem_map.get(addr, 0)
                test_field = 0  # Miss

            # Append the read request and expected response to the message list
            msgs.extend([
                req('rd', i, addr, 0, 0),           # Read request
                resp('rd', i, test_field, 0, expected_data),  # Expected read response
            ])
    return msgs

def stride_with_random_data_msgs():
    # Initialize the random seed for reproducibility
    seed(0xdeadbeef)
    
    # Initialize the address-data map to keep track of written data
    addr_data_map = {}
    base_addr = 0x00001000  # Starting address
    num_accesses = 64       # Number of accesses to perform
    stride = 8              # Stride value in words (32 bytes)
    
    # Build initial memory map
    data_random_list = data_random()
    initial_mem_map = {}
    for i in range(0, len(data_random_list), 2):
        addr = data_random_list[i]
        data = data_random_list[i+1]
        initial_mem_map[addr] = data
    
    # Generate the test messages
    msgs = []
    for i in range(num_accesses):
        addr = base_addr + i * stride * 4  # Addresses with specified stride
        req_type = 'wr' if i % 2 == 0 else 'rd'  # Alternate between write and read
        
        if req_type == 'wr':
            # Generate random data for write operations
            data = randint(0, 0xFFFFFFFF)
            addr_data_map[addr] = data  # Update the data map with the new data
            # Append the write request and expected response to the message list
            msgs.extend([
                req('wr', i, addr, 0, data),  # Write request
                resp('wr', i, 0, 0, 0),       # Expected write response (test field is 0)
            ])
        else:
            # For read operations
            if addr in addr_data_map:
                # If address has been written before, expect a hit
                expected_data = addr_data_map[addr]
                test_field = 1  # Hit
            else:
                # If address hasn't been written before, expect a miss
                expected_data = initial_mem_map.get(addr, 0)
                test_field = 0  # Miss
    
            # Append the read request and expected response to the message list
            msgs.extend([
                req('rd', i, addr, 0, 0),                    # Read request
                resp('rd', i, test_field, 0, expected_data),  # Expected read response
            ])
    return msgs

def unit_stride_shared_data_msgs():
    # Initialize the random seed for reproducibility
    seed(0xdeadbeef)
    
    # Initialize the address-data map to keep track of written data
    addr_data_map = {}
    base_addr = 0x00001000  # Starting address for unit stride access
    num_accesses = 100      # Total number of accesses
    
    # Build initial memory map
    data_random_list = data_random()
    initial_mem_map = {}
    for i in range(0, len(data_random_list), 2):
        addr = data_random_list[i]
        data = data_random_list[i+1]
        initial_mem_map[addr] = data
    
    # Define shared addresses (first 8 addresses)
    shared_addrs = [base_addr + i * 4 for i in range(8)]  # Addresses with high temporal locality
    
    # Generate the test messages
    msgs = []
    for i in range(num_accesses):
        if i % 10 == 0:
            # Every 10 accesses, read from a shared address to introduce temporal locality
            addr = choice(shared_addrs)
            req_type = 'rd'  # Read shared data
        else:
            # Proceed with unit stride access
            addr = base_addr + i * 4  # Sequential addresses with word (4-byte) stride
            req_type = 'wr' if i % 2 == 0 else 'rd'  # Alternate between write and read
            
        if req_type == 'wr':
            # Generate random data for write operations
            data = randint(0, 0xFFFFFFFF)
            addr_data_map[addr] = data  # Update the data map with the new data
            # Append the write request and expected response to the message list
            msgs.extend([
                req('wr', i, addr, 0, data),  # Write request
                resp('wr', i, 0, 0, 0),       # Expected write response
            ])
        else:
            # For read operations
            if addr in addr_data_map:
                # If address has been written before, expect a hit
                expected_data = addr_data_map[addr]
                test_field = 1  # Hit
            else:
                # If address hasn't been written before, expect a miss
                expected_data = initial_mem_map.get(addr, 0)
                test_field = 0  # Miss
                
            # Append the read request and expected response to the message list
            msgs.extend([
                req('rd', i, addr, 0, 0),                    # Read request
                resp('rd', i, test_field, 0, expected_data),  # Expected read response
            ])
    return msgs

test_case_table_random = mk_test_case_table([
  (                                                   "msg_func                                                mem_data_func stall lat src sink"),
  [ "simple_pattern_single_req_random",              simple_pattern_single_req_random_msgs,                 data_random,     0.0,  0,  0,  0    ],
  [ "simple_pattern_single_req_random_sink_delay",   simple_pattern_single_req_random_msgs,                 data_random,     0.9,  3,  0,  10   ],
  [ "simple_pattern_single_req_random_src_delay",    simple_pattern_single_req_random_msgs,                 data_random,     0.9,  3,  10, 0    ],
  [ "simple_pattern_random_req_data",                simple_pattern_random_req_data_msg,                    data_random,     0.0,  0,  0,  0    ],
  [ "simple_pattern_random_req_data_sink_delay",     simple_pattern_random_req_data_msg,                    data_random,     0.9,  3,  0,  10   ],
  [ "simple_pattern_random_req_data_src_delay",      simple_pattern_random_req_data_msg,                    data_random,     0.9,  3,  10, 0    ],
  [ "random_pattern_random_req_data",                random_pattern_random_req_data_msg,                    data_random,     0.0,  0,  0,  0    ],
  [ "random_pattern_random_req_data_sink_delay",     random_pattern_random_req_data_msg,                    data_random,     0.9,  3,  0,  10   ],
  [ "random_pattern_random_req_data_src_delay",      random_pattern_random_req_data_msg,                    data_random,     0.9,  3,  10, 0    ],
  [ "unit_stride_random_data",                       unit_stride_random_data_msgs,                          data_random,     0.0,  0,  0,  0    ],
  [ "unit_stride_random_data_sink_delay",            unit_stride_random_data_msgs,                          data_random,     0.9,  3,  0,  10   ],
  [ "unit_stride_random_data_src_delay",             unit_stride_random_data_msgs,                          data_random,     0.9,  3,  10, 0    ],
  [ "stride_with_random_data",                       stride_with_random_data_msgs,                          data_random,     0.0,  0,  0,  0    ],
  [ "stride_with_random_data_sink_delay",            stride_with_random_data_msgs,                          data_random,     0.9,  3,  0,  10   ],
  [ "stride_with_random_data_src_delay",             stride_with_random_data_msgs,                          data_random,     0.9,  3,  10, 0    ],
  [ "unit_stride_shared_data",                       unit_stride_shared_data_msgs,                          data_random,     0.0,  0,  0,  0    ],
  [ "unit_stride_shared_data_sink_delay",            unit_stride_shared_data_msgs,                          data_random,     0.9,  3,  0,  10   ],
  [ "unit_stride_shared_data_src_delay",             unit_stride_shared_data_msgs,                          data_random,     0.9,  3,  10, 0    ],
  [ "random_write_read",                             random_write_read_msgs,                                data_random,            0.0,  0,  0,  0    ],
  [ "random_write_read_sink_delay",                  random_write_read_msgs,                                data_random,            0.9,  3,  0,  10   ],
  [ "random_write_read_src_delay",                   random_write_read_msgs,                                data_random,            0.9,  3,  10, 0    ],
  [ "stress_test",                                   stress_test,                                           data_random,            0.0,  0,  0,  0    ],
  [ "stress_test_sink_delay",                        stress_test,                                           data_random,            0.9,  3,  0,  10   ],
  [ "stress_test_src_delay",                         stress_test,                                           data_random,            0.9,  3,  10, 0    ],
  [ "random_stress_test",                            random_stress_test,                                    data_random,            0.0,  0,  0,  0    ],
  [ "random_stress_test_sink_delay",                 random_stress_test,                                    data_random,            0.9,  3,  0,  10   ],
  [ "random_stress_test_src_delay",                  random_stress_test,                                    data_random,            0.9,  3,  10, 0    ],

])

@pytest.mark.parametrize( **test_case_table_random )
def test_random( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Cases for Direct Mapped
#-------------------------------------------------------------------------

def conflict_miss_test_dmap():
    return [
        #    type  opq  addr      len data             type  opq  test len data
        req('wr', 0x0, 0x00001000, 0, 0x11111111), resp('wr', 0x0, 0, 0, 0),  # write 0x00001000
        req('wr', 0x1, 0x00001004, 0, 0x22222222), resp('wr', 0x1, 1, 0, 0),  # write 0x00001004
        req('wr', 0x2, 0x00001008, 0, 0x33333333), resp('wr', 0x2, 1, 0, 0),  # write 0x00001008
        req('wr', 0x3, 0x00001100, 0, 0x44444444), resp('wr', 0x3, 0, 0, 0),  # write 0x00001000
        req('wr', 0x4, 0x00001104, 0, 0x55555555), resp('wr', 0x4, 1, 0, 0),  # write 0x00001004
        req('wr', 0x5, 0x00001108, 0, 0x66666666), resp('wr', 0x5, 1, 0, 0),  # write 0x00001008

        # conflict miss
        req('rd', 0x6, 0x00001000, 0, 0), resp('rd', 0x6, 0, 0, 0x11111111),  # (conflict miss)
        req('rd', 0x7, 0x00001100, 0, 0), resp('rd', 0x7, 0, 0, 0x44444444),  # (conflict miss)
        req('wr', 0x8, 0x00000100, 0, 0), resp('wr', 0x8, 0, 0, 0),  # (conflict miss)
        
    ]

def write_read_test_dmap():
    msgs = []
    
    for i in range(16):  # 
        # 
        addr = 0x00001000 + i * 16
        data = 0x1000 + i  # 

        #  miss
        msgs.extend([
            req('wr', i * 4,     addr, 0, data),  resp('wr',     i * 4, 0, 0, 0),   #  miss
            req('rd', i * 4 + 1, addr, 0, 0), resp('rd', i * 4 + 1, 1, 0, data),   #  hit
            req('rd', i * 4 + 2, addr, 0, 0), resp('rd', i * 4 + 2, 1, 0, data),   #  hit
            req('rd', i * 4 + 3, addr, 0, 0), resp('rd', i * 4 + 3, 1, 0, data),   #  hit
        ])

    return msgs

test_case_table_dmap = mk_test_case_table([
  (                                             "msg_func                         mem_data_func stall lat src sink"),
  [ "conflict_miss_dmap_test",            conflict_miss_test_dmap,                None,         0.0,  0,  0,  0    ],
  [ "conflict_miss_dmap_test_sink_delay", conflict_miss_test_dmap,                None,         0.9,  3,  0,  10   ],
  [ "conflict_miss_dmap_test_src_delay",  conflict_miss_test_dmap,                None,         0.9,  3,  10, 0    ],
  [ "write_read_msgs",                       write_read_test_dmap,                None,         0.0,  0,  0,  0    ],
  [ "write_read_msgs_sink_delay",            write_read_test_dmap,                None,         0.9,  3,  0,  10   ],
  [ "write_read_msgs_src_delay",             write_read_test_dmap,                None,         0.9,  3,  10, 0    ],

])

@pytest.mark.parametrize( **test_case_table_dmap )
def test_dmap( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Cases for Set Associative
#-------------------------------------------------------------------------

def conflict_miss_test_sassoc():
    return [
        #    type  opq  addr      len data             type  opq  test len data
        req('wr', 0x0, 0x00001000, 0, 0x11111111), resp('wr', 0x0, 0, 0, 0),  # write 0x00001000 (way 0)
        req('wr', 0x1, 0x00001004, 0, 0x22222222), resp('wr', 0x1, 1, 0, 0),  # write 0x00001004 (way 0)
        req('wr', 0x2, 0x00001008, 0, 0x33333333), resp('wr', 0x2, 1, 0, 0),  # write 0x00001008 (way 0)
        req('wr', 0x3, 0x00001100, 0, 0x44444444), resp('wr', 0x3, 0, 0, 0),  # write 0x00001000 (way 1)
        req('wr', 0x4, 0x00001104, 0, 0x55555555), resp('wr', 0x4, 1, 0, 0),  # write 0x00001004 (way 1)
        req('wr', 0x5, 0x00001108, 0, 0x66666666), resp('wr', 0x5, 1, 0, 0),  # write 0x00001008 (way 1)

        # conflict miss
        req('rd', 0x6, 0x00001000, 0, 0), resp('rd', 0x6, 1, 0, 0x11111111),  # (used to be conflict miss)
        req('rd', 0x7, 0x00001100, 0, 0), resp('rd', 0x7, 1, 0, 0x44444444),  # (used to be conflict miss)
        req('wr', 0x8, 0x00000100, 0, 0), resp('wr', 0x8, 0, 0, 0),  # (conflict miss need more associativity)
    ]

def LRU_replacement_policy():
    # Define the number of cache lines and the size of each line
    num_lines = 8
    line_size = 4  # Number of words per cache line
    
    # Step 1: Write data to fill the cache completely
    msgs = []
    for i in range(num_lines):
        addr_base = 0x00001000 + i * line_size * 4  # Base address for each line
        data = 0x1000 + i  # Initial data value for each line
        for j in range(line_size):
            addr = addr_base + j * 4  # Address of each word in the line
            opq = i * line_size + j  # Unique identifier for each request
            # Write each word to the cache and expect a response
            msgs.extend([
                req('wr', opq, addr, 0, data + j), resp('wr', opq, 0 if j == 0 else 1, 0, 0)
            ])
    
    # Step 2: Read some cache lines to update their access time
    # This makes these lines the most recently used
    for i in range(2):
        addr_base = 0x00001000 + i * line_size * 4
        for j in range(line_size):
            addr = addr_base + j * 4
            opq = i * line_size + j + 100
            # Read each word in the line to update access time
            msgs.extend([
                req('rd', opq, addr, 0, 0), resp('rd', opq, 1, 0, 0x1000 + i + j)
            ])
    
    # Step 3: Write a new line to trigger replacement
    # This new line address differs from the previous ones and should trigger LRU replacement
    new_addr_base = 0x00002000
    for j in range(line_size):
        addr = new_addr_base + j * 4
        opq = num_lines * line_size + j
        data = 0x2000 + j
        # Write each word in the new line, which should cause an eviction of the least recently used line
        msgs.extend([
            req('wr', opq, addr, 0, data), resp('wr', opq, 0 if j == 0 else 1, 0, 0)
        ])
    
    # Step 4: Verify that the least recently used line has been replaced
    # Read from the original lines that were not accessed in Step 2 to confirm they've been evicted
    old_addr_base = 0x00001000 + 2 * line_size * 4
    for j in range(line_size):
        addr = old_addr_base + j * 4
        opq = num_lines * line_size + j + 100
        # Attempt to read the evicted line, which should now miss and reload from main memory
        msgs.extend([
            req('rd', opq, addr, 0, 0), resp('rd', opq, 1, 0, 0x1000 + 2 + j)
        ])
    
    return msgs

def corner_case_both_tags_not_match_test():
  
    return [
        #    type  opq  addr      len data             type  opq  test len data
        req('wr', 0x0, 0x00001000, 0, 0x11111111), resp('wr', 0x0, 0, 0, 0),  # Write to address 0x00001000 (way 0)
        req('wr', 0x1, 0x00002000, 0, 0x22222222), resp('wr', 0x1, 0, 0, 0),  # Write to a different address(way 1)
        req('wr', 0x2, 0x00001100, 0, 0x33333333), resp('wr', 0x2, 0, 0, 0),  # Write to a different address(update way 0)
        req('rd', 0x3, 0x00001000, 0, 0), resp('rd', 0x3, 0, 0, 0x11111111),  # both tags not match update way 1
        req('rd', 0x4, 0x00002000, 0, 0), resp('rd', 0x4, 0, 0, 0x22222222),  # both tags not match update way 0
        req('rd', 0x5, 0x00001100, 0, 0), resp('rd', 0x5, 0, 0, 0x33333333),  # both tags not match update way 1
    ]

test_case_table_sassoc = mk_test_case_table([
  (                                   "msg_func                                       mem_data_func    stall lat src sink"),
  [ "conflict_miss_test",             conflict_miss_test_sassoc,                             None, 0.0,  0,  0,  0    ],
  [ "conflict_miss_test_sink_delay",  conflict_miss_test_sassoc,                             None, 0.9,  3,  0,  10   ],
  [ "conflict_miss_test_src_delay",   conflict_miss_test_sassoc,                             None, 0.9,  3,  10, 0    ],
  [ "LRU_replacement_policy",         LRU_replacement_policy,                                None, 0.0,  0,  0,  0    ],
  [ "LRU_replacement_policy_sink_delay", LRU_replacement_policy,                             None, 0.9,  3,  0,  10   ],
  [ "LRU_replacement_policy_src_delay",  LRU_replacement_policy,                             None, 0.9,  3,  10, 0    ],
  [ "corner_case_both_tags_not_match_test",  corner_case_both_tags_not_match_test,           None, 0.0,  0,  0,  0    ],
  [ "corner_case_both_tags_not_match_test_sink_delay",  corner_case_both_tags_not_match_test,None, 0.9,  3,  0,  10   ],
  [ "corner_case_both_tags_not_match_test_src_delay",  corner_case_both_tags_not_match_test, None, 0.9,  3,  10, 0    ],

])

@pytest.mark.parametrize( **test_case_table_sassoc )
def test_sassoc( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Banked cache test
#-------------------------------------------------------------------------
# This test case is to test if the bank offset is implemented correctly.
# The idea behind this test case is to differentiate between a cache with
# no bank bits and a design has one/two bank bits by looking at cache
# request hit/miss status.

# We first design a test case for 2-way set-associative cache. The last
# request should hit only if students implement the correct index bit to
# be [6:9]. If they implement the index bit to be [4:7] or [5:8], the
# last request is a miss, which is wrong. See below for explanation. This
# test case also works for the baseline direct-mapped cache.

# Direct-mapped
#
#   no bank(should fail):
#      idx
#   00 0000 0000
#   01 0000 0000
#   10 0000 0000
#   00 0000 0000
#   idx: 0, 0, 0 so the third one with tag 10 will evict the first one
#   with tag 00, and thus the fourth read will miss instead of hit.
#
#   4-bank(correct):
#    idx  bk
#   00 00 00 0000
#   01 00 00 0000
#   10 00 00 0000
#   00 00 00 0000
#   idx: 0, 4, 8 so the third one with tag 10 won't evict anything, and
#   thus the fourth read will hit.

# 2-way set-associative
#
#   no bank(should fail):
#        idx
#   00 0 000 0000
#   01 0 000 0000
#   10 0 000 0000
#   00 0 000 0000
#   idx: 0, 0, 0 so the third one with tag 10 will evict the first one
#   with tag 00, and thus the fourth read will miss instead of hit.
#
#   4-bank(correct):
#     idx  bk
#   0 0 00 00 0000
#   0 1 00 00 0000
#   1 0 00 00 0000
#   idx: 0, 4, 0 so the third one with tag 10 won't evict anything, and
#   thus the fourth read will hit.

def bank_test():
  return [
    #    type  opq  addr      len data        type  opq  test len data
    req( 'rd', 0x0, 0x00000000, 0, 0 ), resp( 'rd', 0x0, 0,   0,  0xdeadbeef ),
    req( 'rd', 0x1, 0x00000100, 0, 0 ), resp( 'rd', 0x1, 0,   0,  0x00c0ffee ),
    req( 'rd', 0x2, 0x00000200, 0, 0 ), resp( 'rd', 0x2, 0,   0,  0xffffffff ),
    req( 'rd', 0x3, 0x00000000, 0, 0 ), resp( 'rd', 0x3, 1,   0,  0xdeadbeef ),
  ]

def four_bank_write_read_hit():
    return [
        req('wr', 0x0, 0x1000, 0, 0x12345678), resp('wr', 0x0, 0, 0, 0),
        req('rd', 0x1, 0x1000, 0, 0), resp('rd', 0x1, 1, 0, 0x12345678),
    ]

def bank_test_data():
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000100, 0x00c0ffee,
    0x00000200, 0xffffffff,
  ]

test_case_table_bank = mk_test_case_table([
  (             "msg_func                 mem_data_func   stall lat src sink"),
  [ "bank_test", bank_test,               bank_test_data, 0.0,  0,  0,  0    ],
  [ "bank_test_sink_delay", bank_test,    bank_test_data, 0.9,  3,  0,  10   ],
  [ "bank_test_src_delay", bank_test,     bank_test_data, 0.9,  3,  10, 0    ],
  [ "four_bank_write_read_hit", four_bank_write_read_hit, None, 0.0,  0,  0,  0    ],
  [ "four_bank_write_read_hit_sink_delay", four_bank_write_read_hit, None, 0.9,  3,  0,  10   ],
  [ "four_bank_write_read_hit_src_delay", four_bank_write_read_hit, None, 0.9,  3,  10, 0    ],


])

@pytest.mark.parametrize( **test_case_table_bank )
def test_bank( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )
