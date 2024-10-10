#=========================================================================
# proc_sim_test
#=========================================================================
# Make sure that proc-sim works.

import pytest
import os

from subprocess import check_call, CalledProcessError

impls  = [ "fl", "base" ]
inputs = [ "vvadd-unopt", "vvadd-opt", "cmult", "mfilt", "bsearch" ]

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Once you get your baseline and alternative design passing all of your
# tests and once you have your processor working, then update the impls
# list to include "base" and "alt" so that this test case will help make
# sure your simulator is always working. You can do that by adding
# something like this:
#
#  impls += [ "base", "alt" ]
#
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

test_cases = []
for input_ in inputs:
  for impl in impls:
    test_cases.append([ impl, input_ ])

@pytest.mark.parametrize( "impl,input_", test_cases )
def test( impl, input_, cmdline_opts ):

  # Get path to simulator script

  test_dir = os.path.dirname( os.path.abspath( __file__ ) )
  sim_dir  = os.path.dirname( test_dir )
  sim      = sim_dir + os.path.sep + 'proc-sim'

  # Command

  cmd = [ sim, "--impl", impl, "--input", input_, "--verify" ]

  # Display simulator command line

  print("")
  print("Simulator command line:", ' '.join(cmd))

  # Run the sprocator

  try:
    check_call(cmd)
  except CalledProcessError as e:
    raise Exception( "Error running simulator!" )

