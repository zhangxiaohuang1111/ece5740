#=========================================================================
# SingleCoreSysFL_test.py
#=========================================================================
# We apply select tests from lab2 to the single core system.

import pytest

from pymtl3 import *

from lab4_sys.test.harness import asm_test
from lab4_sys.test.harness import run_score_test as run_test

from lab4_sys.SingleCoreSysFL import SingleCoreSysFL

from lab2_proc.test import inst_csr
from lab2_proc.test import inst_add
from lab2_proc.test import inst_sub
from lab2_proc.test import inst_mul
from lab2_proc.test import inst_and
from lab2_proc.test import inst_or
from lab2_proc.test import inst_xor
from lab2_proc.test import inst_slt
from lab2_proc.test import inst_sltu
from lab2_proc.test import inst_sra
from lab2_proc.test import inst_srl
from lab2_proc.test import inst_sll
from lab2_proc.test import inst_addi
from lab2_proc.test import inst_andi
from lab2_proc.test import inst_ori
from lab2_proc.test import inst_xori
from lab2_proc.test import inst_slti
from lab2_proc.test import inst_sltiu
from lab2_proc.test import inst_srai
from lab2_proc.test import inst_srli
from lab2_proc.test import inst_slli
from lab2_proc.test import inst_lui
from lab2_proc.test import inst_auipc
from lab2_proc.test import inst_lw
from lab2_proc.test import inst_sw
from lab2_proc.test import inst_beq
from lab2_proc.test import inst_bne
from lab2_proc.test import inst_bge
from lab2_proc.test import inst_bgeu
from lab2_proc.test import inst_blt
from lab2_proc.test import inst_bltu
from lab2_proc.test import inst_jal
from lab2_proc.test import inst_jalr

#''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Import additional files from lab2_proc.test as necessary
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

@pytest.mark.usefixtures("cmdline_opts")
class Tests:

  @classmethod
  def setup_class( cls ):
    cls.SysType = SingleCoreSysFL

  #-----------------------------------------------------------------------
  # csr
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_csr.gen_basic_test      ),
    asm_test( inst_csr.gen_bypass_test     ),
    asm_test( inst_csr.gen_value_test      ),
    asm_test( inst_csr.gen_random_test     ),
    asm_test( inst_csr.gen_core_stats_test ),
  ])
  def test_csr( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_csr_delays( s ):
    run_test( s.SysType, inst_csr.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # add
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_add.gen_basic_test     ),
    asm_test( inst_add.gen_dest_dep_test  ),
    asm_test( inst_add.gen_src0_dep_test  ),
    asm_test( inst_add.gen_src1_dep_test  ),
    asm_test( inst_add.gen_srcs_dep_test  ),
    asm_test( inst_add.gen_srcs_dest_test ),
    asm_test( inst_add.gen_value_test     ),
    asm_test( inst_add.gen_random_test    ),
  ])
  def test_add( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_add_delays( s ):
    run_test( s.SysType, inst_add.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # sub
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_sub.gen_basic_test     ),
    asm_test( inst_sub.gen_dest_dep_test  ),
    asm_test( inst_sub.gen_src0_dep_test  ),
    asm_test( inst_sub.gen_src1_dep_test  ),
    asm_test( inst_sub.gen_srcs_dep_test  ),
    asm_test( inst_sub.gen_srcs_dest_test ),
    asm_test( inst_sub.gen_value_test     ),
    asm_test( inst_sub.gen_random_test    ),
  ])

  def test_sub( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_sub_delays( s ):
    run_test( s.SysType, inst_sub.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # mul
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_mul.gen_basic_test     ),
    asm_test( inst_mul.gen_dest_dep_test  ),
    asm_test( inst_mul.gen_src0_dep_test  ),
    asm_test( inst_mul.gen_src1_dep_test  ),
    asm_test( inst_mul.gen_srcs_dep_test  ),
    asm_test( inst_mul.gen_srcs_dest_test ),
    asm_test( inst_mul.gen_value_test     ),
    asm_test( inst_mul.gen_random_test    ),
  ])

  def test_mul( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_mul_delays( s ):
    run_test( s.SysType, inst_sub.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
    
  #-----------------------------------------------------------------------
  # and
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_and.gen_basic_test     ),
    asm_test( inst_and.gen_dest_dep_test  ),
    asm_test( inst_and.gen_src0_dep_test  ),
    asm_test( inst_and.gen_src1_dep_test  ),
    asm_test( inst_and.gen_srcs_dep_test  ),
    asm_test( inst_and.gen_srcs_dest_test ),
    asm_test( inst_and.gen_value_test     ),
    asm_test( inst_and.gen_random_test    ),
  ])
  
  def test_and( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_and_delays( s ):
    run_test( s.SysType, inst_and.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # or
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_or.gen_basic_test     ),
    asm_test( inst_or.gen_dest_dep_test  ),
    asm_test( inst_or.gen_src0_dep_test  ),
    asm_test( inst_or.gen_src1_dep_test  ),
    asm_test( inst_or.gen_srcs_dep_test  ),
    asm_test( inst_or.gen_srcs_dest_test ),
    asm_test( inst_or.gen_value_test     ),
    asm_test( inst_or.gen_random_test    ),
  ])

  def test_or( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_or_delays( s ):
    run_test( s.SysType, inst_or.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # xor
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_xor.gen_basic_test     ),
    asm_test( inst_xor.gen_dest_dep_test  ),
    asm_test( inst_xor.gen_src0_dep_test  ),
    asm_test( inst_xor.gen_src1_dep_test  ),
    asm_test( inst_xor.gen_srcs_dep_test  ),
    asm_test( inst_xor.gen_srcs_dest_test ),
    asm_test( inst_xor.gen_value_test     ),
    asm_test( inst_xor.gen_random_test    ),
  ])

  def test_xor( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_xor_delays( s ):
    run_test( s.SysType, inst_xor.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # slt
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_slt.gen_basic_test     ),
    asm_test( inst_slt.gen_dest_dep_test  ),
    asm_test( inst_slt.gen_src0_dep_test  ),
    asm_test( inst_slt.gen_src1_dep_test  ),
    asm_test( inst_slt.gen_srcs_dep_test  ),
    asm_test( inst_slt.gen_srcs_dest_test ),
    asm_test( inst_slt.gen_value_test     ),
    asm_test( inst_slt.gen_random_test    ),
  ])

  def test_slt( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_slt_delays( s ):
    run_test( s.SysType, inst_slt.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # sltu
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_sltu.gen_basic_test     ),
    asm_test( inst_sltu.gen_dest_dep_test  ),
    asm_test( inst_sltu.gen_src0_dep_test  ),
    asm_test( inst_sltu.gen_src1_dep_test  ),
    asm_test( inst_sltu.gen_srcs_dep_test  ),
    asm_test( inst_sltu.gen_srcs_dest_test ),
    asm_test( inst_sltu.gen_value_test     ),
    asm_test( inst_sltu.gen_random_test    ),
  ])

  def test_sltu( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_sltu_delays( s ):
    run_test( s.SysType, inst_sltu.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # sra
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_sra.gen_basic_test     ),
    asm_test( inst_sra.gen_dest_dep_test  ),
    asm_test( inst_sra.gen_src0_dep_test  ),
    asm_test( inst_sra.gen_src1_dep_test  ),
    asm_test( inst_sra.gen_srcs_dep_test  ),
    asm_test( inst_sra.gen_srcs_dest_test ),
    asm_test( inst_sra.gen_value_test     ),
    asm_test( inst_sra.gen_random_test    ),
  ])

  def test_sra( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_sra_delays( s ):
    run_test( s.SysType, inst_sra.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # srl
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_srl.gen_basic_test     ),
    asm_test( inst_srl.gen_dest_dep_test  ),
    asm_test( inst_srl.gen_src0_dep_test  ),
    asm_test( inst_srl.gen_src1_dep_test  ),
    asm_test( inst_srl.gen_srcs_dep_test  ),
    asm_test( inst_srl.gen_srcs_dest_test ),
    asm_test( inst_srl.gen_value_test     ),
    asm_test( inst_srl.gen_random_test    ),
  ])

  def test_srl( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_srl_delays( s ):
    run_test( s.SysType, inst_srl.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # sll
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_sll.gen_basic_test     ),
    asm_test( inst_sll.gen_dest_dep_test  ),
    asm_test( inst_sll.gen_src0_dep_test  ),
    asm_test( inst_sll.gen_src1_dep_test  ),
    asm_test( inst_sll.gen_srcs_dep_test  ),
    asm_test( inst_sll.gen_srcs_dest_test ),
    asm_test( inst_sll.gen_value_test     ),
    asm_test( inst_sll.gen_random_test    ),
  ])

  def test_sll( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_sll_delays( s ):
    run_test( s.SysType, inst_sll.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # addi
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_addi.gen_basic_test     ) ,
    asm_test( inst_addi.gen_dest_dep_test  ) ,
    asm_test( inst_addi.gen_src_dep_test   ) ,
    asm_test( inst_addi.gen_srcs_dest_test ) ,
    asm_test( inst_addi.gen_value_test     ) ,
    asm_test( inst_addi.gen_random_test    ) ,
  ])

  def test_addi( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_addi_delays( s ):
    run_test( s.SysType, inst_andi.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # andi
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_andi.gen_basic_test     ) ,
    asm_test( inst_andi.gen_dest_dep_test  ) ,
    asm_test( inst_andi.gen_src_dep_test   ) ,
    asm_test( inst_andi.gen_srcs_dest_test ) ,
    asm_test( inst_andi.gen_value_test     ) ,
    asm_test( inst_andi.gen_random_test    ) ,
  ])

  def test_andi( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_andi_delays( s ):
    run_test( s.SysType, inst_andi.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # ori
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_ori.gen_basic_test     ) ,
    asm_test( inst_ori.gen_dest_dep_test  ) ,
    asm_test( inst_ori.gen_src_dep_test   ) ,
    asm_test( inst_ori.gen_srcs_dest_test ) ,
    asm_test( inst_ori.gen_value_test     ) ,
    asm_test( inst_ori.gen_random_test    ) ,
  ])

  def test_ori( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_ori_delays( s ):
    run_test( s.SysType, inst_ori.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # xori
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_xori.gen_basic_test     ) ,
    asm_test( inst_xori.gen_dest_dep_test  ) ,
    asm_test( inst_xori.gen_src_dep_test   ) ,
    asm_test( inst_xori.gen_srcs_dest_test ) ,
    asm_test( inst_xori.gen_value_test     ) ,
    asm_test( inst_xori.gen_random_test    ) ,
  ])

  def test_xori( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_xori_delays( s ):
    run_test( s.SysType, inst_xori.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # slti
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_slti.gen_basic_test     ) ,
    asm_test( inst_slti.gen_dest_dep_test  ) ,
    asm_test( inst_slti.gen_src_dep_test   ) ,
    asm_test( inst_slti.gen_srcs_dest_test ) ,
    asm_test( inst_slti.gen_value_test     ) ,
    asm_test( inst_slti.gen_random_test    ) ,
  ])

  def test_slti( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_slti_delays( s ):
    run_test( s.SysType, inst_slti.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # sltiu
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_sltiu.gen_basic_test     ) ,
    asm_test( inst_sltiu.gen_dest_dep_test  ) ,
    asm_test( inst_sltiu.gen_src_dep_test   ) ,
    asm_test( inst_sltiu.gen_srcs_dest_test ) ,
    asm_test( inst_sltiu.gen_value_test     ) ,
    asm_test( inst_sltiu.gen_random_test    ) ,
  ])

  def test_sltiu( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )
  
  def test_sltiu_delays( s ):
    run_test( s.SysType, inst_sltiu.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # srai
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_srai.gen_basic_test     ) ,
    asm_test( inst_srai.gen_dest_dep_test  ) ,
    asm_test( inst_srai.gen_src_dep_test   ) ,
    asm_test( inst_srai.gen_srcs_dest_test ) ,
    asm_test( inst_srai.gen_value_test     ) ,
    asm_test( inst_srai.gen_random_test    ) ,

  ])

  def test_srai( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_srai_delays( s ):
    run_test( s.SysType, inst_srai.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # srli
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_srli.gen_basic_test     ) ,
    asm_test( inst_srli.gen_dest_dep_test  ) ,
    asm_test( inst_srli.gen_src_dep_test   ) ,
    asm_test( inst_srli.gen_srcs_dest_test ) ,
    asm_test( inst_srli.gen_value_test     ) ,
    asm_test( inst_srli.gen_random_test    ) ,
  ])
  def test_srli( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_srli_delays( s ):
    run_test( s.SysType, inst_srli.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # slli
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_slli.gen_basic_test     ) ,
    asm_test( inst_slli.gen_dest_dep_test  ) ,
    asm_test( inst_slli.gen_src_dep_test   ) ,
    asm_test( inst_slli.gen_srcs_dest_test ) ,
    asm_test( inst_slli.gen_value_test     ) ,
    asm_test( inst_slli.gen_random_test    ) ,
  ])

  def test_slli( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_slli_delays( s ):
    run_test( s.SysType, inst_slli.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # lui
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_lui.gen_basic_test    ) ,
    asm_test( inst_lui.gen_dest_dep_test ) ,
    asm_test( inst_lui.gen_value_test    ) ,
    asm_test( inst_lui.gen_random_test   ) ,
  ])
  def test_lui( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_lui_delays( s ):
    run_test( s.SysType, inst_lui.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # auipc
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_auipc.gen_basic_test    ) ,
    asm_test( inst_auipc.gen_dest_dep_test) ,
    asm_test( inst_auipc.gen_value_test   ) ,
    asm_test( inst_auipc.gen_auipc_random_test  ) ,

  ])
  def test_auipc( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_auipc_delays( s ):
    run_test( s.SysType, inst_auipc.gen_auipc_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # lw
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_lw.gen_basic_test     ) ,
    asm_test( inst_lw.gen_dest_dep_test  ) ,
    asm_test( inst_lw.gen_base_dep_test  ) ,
    asm_test( inst_lw.gen_srcs_dest_test ) ,
    asm_test( inst_lw.gen_addr_test      ) ,
    asm_test( inst_lw.gen_random_test    ) ,
  ])
  def test_lw( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_lw_delays( s ):
    run_test( s.SysType, inst_lw.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # sw
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_sw.gen_basic_test     ),
    asm_test( inst_sw.gen_basic_test     ),
    asm_test( inst_sw.gen_dest_dep_test  ) ,
    asm_test( inst_sw.gen_base_dep_test  ) ,
    asm_test( inst_sw.gen_srcs_dest_test ) ,
    asm_test( inst_sw.gen_addr_test      ) ,
    asm_test( inst_sw.gen_random_test    ) ,
  ])
  def test_sw( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_sw_delays( s ):
    run_test( s.SysType, inst_sw.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )


  #-----------------------------------------------------------------------
  # beq
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_beq.gen_basic_test ) ,
    asm_test( inst_beq.gen_src0_dep_taken_test ) ,
    asm_test( inst_beq.gen_src0_dep_nottaken_test ) ,
    asm_test( inst_beq.gen_src1_dep_taken_test ) ,
    asm_test( inst_beq.gen_src1_dep_nottaken_test ) ,
    asm_test( inst_beq.gen_srcs_dep_taken_test ) ,
    asm_test( inst_beq.gen_srcs_dep_nottaken_test ) ,
    asm_test( inst_beq.gen_src0_eq_src1_test ) ,
    asm_test( inst_beq.gen_value_test ) ,
    asm_test( inst_beq.gen_random_test ) ,
    asm_test( inst_beq.gen_back_to_back_test ) ,
  ])
   
  def test_beq( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_beq_delays( s ):
    run_test( s.SysType, inst_beq.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # bne
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_bne.gen_basic_test             ),
    asm_test( inst_bne.gen_src0_dep_taken_test    ),
    asm_test( inst_bne.gen_src0_dep_nottaken_test ),
    asm_test( inst_bne.gen_src1_dep_taken_test    ),
    asm_test( inst_bne.gen_src1_dep_nottaken_test ),
    asm_test( inst_bne.gen_srcs_dep_taken_test    ),
    asm_test( inst_bne.gen_srcs_dep_nottaken_test ),
    asm_test( inst_bne.gen_src0_eq_src1_test      ),
    asm_test( inst_bne.gen_value_test             ),
    asm_test( inst_bne.gen_random_test            ),
    asm_test( inst_bne.gen_back_to_back_test      ),
  ])
  def test_bne( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_bne_delays( s ):
    run_test( s.SysType, inst_bne.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # bge
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_bge.gen_basic_test             ),
    asm_test( inst_bge.gen_src0_dep_taken_test    ),
    asm_test( inst_bge.gen_src0_dep_nottaken_test ),
    asm_test( inst_bge.gen_src1_dep_taken_test    ),
    asm_test( inst_bge.gen_src1_dep_nottaken_test ),
    asm_test( inst_bge.gen_srcs_dep_taken_test    ),
    asm_test( inst_bge.gen_srcs_dep_nottaken_test ),
    asm_test( inst_bge.gen_src0_eq_src1_test      ),
    asm_test( inst_bge.gen_value_test             ),
    asm_test( inst_bge.gen_random_test            ),
    asm_test( inst_bge.gen_back_to_back_test      ),

  ])
  def test_bge( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_bge_delays( s ):
    run_test( s.SysType, inst_bge.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )


  #-----------------------------------------------------------------------
  # bgeu
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_bgeu.gen_basic_test             ),
    asm_test( inst_bgeu.gen_src0_dep_taken_test    ),
    asm_test( inst_bgeu.gen_src0_dep_nottaken_test ),
    asm_test( inst_bgeu.gen_src1_dep_taken_test    ),
    asm_test( inst_bgeu.gen_src1_dep_nottaken_test ),
    asm_test( inst_bgeu.gen_srcs_dep_taken_test    ),
    asm_test( inst_bgeu.gen_srcs_dep_nottaken_test ),
    asm_test( inst_bgeu.gen_src0_eq_src1_test      ),
    asm_test( inst_bgeu.gen_value_test             ),
    asm_test( inst_bgeu.gen_random_test            ),
    asm_test( inst_bgeu.gen_back_to_back_test      ),

  ])
  def test_bgeu( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_bgeu_delays( s ):
    run_test( s.SysType, inst_bgeu.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # blt
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_blt.gen_basic_test             ),
    asm_test( inst_blt.gen_src0_dep_taken_test    ),
    asm_test( inst_blt.gen_src0_dep_nottaken_test ),
    asm_test( inst_blt.gen_src1_dep_taken_test    ),
    asm_test( inst_blt.gen_src1_dep_nottaken_test ),
    asm_test( inst_blt.gen_srcs_dep_taken_test    ),
    asm_test( inst_blt.gen_srcs_dep_nottaken_test ),
    asm_test( inst_blt.gen_src0_eq_src1_test      ),
    asm_test( inst_blt.gen_value_test             ),
    asm_test( inst_blt.gen_random_test            ),
    asm_test( inst_blt.gen_back_to_back_test      ),
   
  ])
  def test_blt( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_blt_delays( s ):
    run_test( s.SysType, inst_blt.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # bltu
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_bltu.gen_basic_test             ),
    asm_test( inst_bltu.gen_src0_dep_taken_test    ),
    asm_test( inst_bltu.gen_src0_dep_nottaken_test ),
    asm_test( inst_bltu.gen_src1_dep_taken_test    ),
    asm_test( inst_bltu.gen_src1_dep_nottaken_test ),
    asm_test( inst_bltu.gen_srcs_dep_taken_test    ),
    asm_test( inst_bltu.gen_srcs_dep_nottaken_test ),
    asm_test( inst_bltu.gen_src0_eq_src1_test      ),
    asm_test( inst_bltu.gen_value_test             ),
    asm_test( inst_bltu.gen_random_test            ),
    asm_test( inst_bltu.gen_back_to_back_test      ),

  ])
  def test_bltu( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_bltu_delays( s ):
    run_test( s.SysType, inst_bltu.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  def gen_branch_jal_test():
    return """
      csrr x1, mngr2proc < 5
      csrr x2, mngr2proc < 4
      addi x4, x0, 0
      nop
      nop
      nop
      nop
      nop
      nop
      nop
      nop
      bne  x1, x2, label_a
      jal  x3, label_b
      nop
      nop
      nop
      nop
    label_b:
      addi x4, x4, 0b10
      nop
      nop
      nop
    label_a:
      addi x4, x4, 0b01
      nop
      nop
      nop
      nop
      csrw proc2mngr, x4 > 0b01
      nop
      nop
      nop
      nop
      nop
      nop
      nop
      nop
    """
  @pytest.mark.parametrize("name, test", [
      asm_test( gen_branch_jal_test )
  ])
  def test_branch_jal(s, name, test):
      run_test(s.SysType, test, cmdline_opts=s.__class__.cmdline_opts  )

  #-----------------------------------------------------------------------
  # jal
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_jal.gen_basic_test      ) ,
    asm_test( inst_jal.gen_multijump_test  ) ,
    asm_test( inst_jal.gen_dest_dep_5_test ) ,
    asm_test( inst_jal.gen_dest_dep_4_test ) ,
    asm_test( inst_jal.gen_dest_dep_3_test ) ,
    asm_test( inst_jal.gen_dest_dep_2_test ) ,
    asm_test( inst_jal.gen_dest_dep_1_test ) ,
    asm_test( inst_jal.gen_dest_dep_0_test ) ,
    asm_test( inst_jal.gen_back_to_back_test ) ,
  ])

  def test_jal( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_jal_delays( s ):
    run_test( s.SysType, inst_jal.gen_back_to_back_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # jalr
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_jalr.gen_basic_test    ),
    asm_test( inst_jalr.gen_dest_dep_5_test ),
    asm_test( inst_jalr.gen_dest_dep_4_test ),
    asm_test( inst_jalr.gen_dest_dep_3_test ),
    asm_test( inst_jalr.gen_dest_dep_2_test ),
    asm_test( inst_jalr.gen_dest_dep_1_test ),
    asm_test( inst_jalr.gen_dest_dep_0_test ),
    asm_test( inst_jalr.gen_src_dep_5_test  ),
    asm_test( inst_jalr.gen_src_dep_4_test  ),
    asm_test( inst_jalr.gen_src_dep_3_test  ),
    asm_test( inst_jalr.gen_src_dep_2_test  ),
    asm_test( inst_jalr.gen_src_dep_1_test  ),
    asm_test( inst_jalr.gen_src_dep_0_test  ),
    asm_test( inst_jalr.gen_src_eq_dest_test ),
    asm_test( inst_jalr.gen_back_to_back_test ),
  ])

  def test_jalr( s, name, test ):
    run_test( s.SysType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_jalr_delays( s ):
      run_test( s.SysType, inst_jalr.gen_back_to_back_test, delays=True,
                cmdline_opts=s.__class__.cmdline_opts )