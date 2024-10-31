//=========================================================================
// Base Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_CACHE_BASE_DPATH_V
`define LAB3_MEM_CACHE_BASE_DPATH_V

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab3_mem_CacheBaseDpath
#(
  parameter p_num_banks = 1
)
(
  input  logic          clk,
  input  logic          reset,

  // Processor <-> Cache Interface

  input  mem_req_4B_t   proc2cache_reqstream_msg,
  output mem_resp_4B_t  proc2cache_respstream_msg,

  // Cache <-> Memory Interface

  output mem_req_16B_t  cache2mem_reqstream_msg,
  input  mem_resp_16B_t cache2mem_respstream_msg,

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Define additional ports
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
);

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement data-path
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  // cachereq_opaque_reg
    vc_EnReg #(
    .p_nbits(8)
  ) cachereq_opaque_reg (
    .clk(clk),
    .reset(reset),
    .d(proc2cache_reqstream_msg.opaque),
    .q(cachereq_opaque),
    .en(cachereq_en)
  );

  // cachereq_type_reg
  vc_EnReg #(
    .p_nbits(4)
  ) cachereq_type_reg (
    .clk(clk),
    .reset(reset),
    .q(cachereq_type),
    .d(proc2cache_reqstream_msg.type_),
    .en(cachereq_en)
  );

  // cachereq_addr_reg
  vc_EnReg #(
    .p_nbits(32)
  ) cachereq_addr_reg (
    .clk(clk),
    .reset(reset),
    .q(cachereq_addr),
    .d(proc2cache_reqstream_msg.addr),
    .en(cachereq_en)
  );

  // cachereq_data_reg
  vc_EnReg #(
    .p_nbits(32)
  ) cachereq_data_reg (
    .clk(clk),
    .reset(reset),
    .q(cachereq_data),
    .d(proc2cache_reqstream_msg.data),
    .en(cachereq_en)
  );

  // memresp_data_reg
  vc_EnReg #(
    .p_nbits(128)
  ) memresp_data_reg (
    .clk(clk),
    .reset(reset),
    .q(memresp_data),
    .d(cache2mem_respstream_msg.data),
    .en(memresp_en)
  );

  // data array
  vc_CombinationalSRAM_1rw #(
    .p_data_nbits(128),          // data width
    .p_num_entries(16)           // cache size
  ) data_array (
    .clk(clk),
    .reset(reset),
    .read_en(data_read_en),
    .read_addr(data_read_addr),
    .read_data(data_read_data),
    .write_en(data_write_en),
    .write_byte_en(data_write_byte_en),
    .write_addr(data_write_addr),
    .write_data(data_write_data)
  );

  // tag array
  vc_CombinationalBitSRAM_1rw #(
    .p_data_nbits(24),          // tag width
    .p_num_entries(16)          // cache size
  ) tag_array (
    .clk(clk),
    .reset(reset),
    .read_en(tag_read_en),
    .read_addr(tag_read_addr),
    .read_data(tag_read_data),
    .write_en(tag_write_en),
    .write_addr(tag_write_addr),
    .write_data(tag_write_data)
  );
endmodule

`endif
