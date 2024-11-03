//=========================================================================
// Base Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_CACHE_BASE_DPATH_V
`define LAB3_MEM_CACHE_BASE_DPATH_V

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

`include "vc/mem-msgs.v"
`include "vc/srams.v"
`include "vc/regs.v"
`include "vc/muxes.v"
`include "vc/arithmetic.v"

`include "lab3_mem/WbenDecoder.v"
`include "lab3_mem/ReplUnit.v"

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

  // control signals (ctrl->dpath)

  input  logic          cachereq_reg_en,
  input  logic          memresp_reg_en,
  input  logic          write_data_mux_sel,
  input  logic          wben_mux_sel,
  input  logic          tag_array_wen,
  input  logic          tag_array_ren,
  input  logic          data_array_wen,
  input  logic          data_array_ren,
  input  logic          read_data_zero_mux_sel,
  input  logic          read_data_reg_en,
  input  logic          evict_addr_reg_en,
  input  logic          memreq_addr_mux_sel,
  input  logic [1:0]    hit,
  input  logic [3:0]    memreq_type,

  // status signals (dpath->ctrl)

  output logic  [3:0]   cachereq_type,
  output logic [31:0]   cachereq_addr,
  output logic          tag_match

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Define additional ports
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
);

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement data-path
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  // Register the unpacked proc2cache_reqstream_msg

  logic [31:0] cachereq_addr_reg_out;
  logic [31:0] cachereq_data_reg_out;
  logic  [2:0] cachereq_type_reg_out;
  logic  [7:0] cachereq_opaque_reg_out;

  vc_EnResetReg #(4,0) cachereq_type_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.type_),
    .q      (cachereq_type_reg_out)
  );

  vc_EnResetReg #(32,0) cachereq_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.addr),
    .q      (cachereq_addr_reg_out)
  );

  vc_EnResetReg #(8,0) cachereq_opaque_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.opaque),
    .q      (cachereq_opaque_reg_out)
  );

  vc_EnResetReg #(32,0) cachereq_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.data),
    .q      (cachereq_data_reg_out)
  );

  assign cachereq_type = cachereq_type_reg_out;
  assign cachereq_addr = cachereq_addr_reg_out;
  
  logic [127:0] memresp_data_reg_out;
  vc_EnResetReg #(128,0) memresp_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (memresp_reg_en),
    .d      (cache2mem_respstream_msg.data),
    .q      (memresp_data_reg_out)
  );

  // Write data mux
  logic [127:0] write_data_mux_out;
  vc_Mux2 #(128) write_data_mux(
  .in1  (cachereq_data_replicated),
  .in0  (memresp_data_reg_out),
  .sel  (write_data_mux_sel),
  .out  (write_data_mux_out)
  );

  // wben_mux
  logic [15:0]  wben_mux_out;
  vc_Mux2 #(16) wben_mux(
  .in1  (wben_decoder_out),
  .in0  (16'hffff),
  .sel  (wben_mux_sel),
  .out  (wben_mux_out)
  );

  //tag comparator
  vc_EqComparator #(24) tag_comparator(
  .in1 (cachereq_addr_tag),
  .in0 (tag_array_read_out),
  .out (tag_match)
  );

  // make_addr
  logic [31:0] make_addr_1;
  logic [31:0] make_addr_0;
  assign make_addr_1 = {tag_array_read_out, cachereq_addr_index, 4'b0};
  assign make_addr_0 = {cachereq_addr_tag, cachereq_addr_index, 4'b0};

  // evict_addr_reg
  logic [31:0] evict_addr_reg_out;
  vc_EnResetReg #(32,0) evict_addr_reg(
  .clk    (clk),
  .reset  (reset),
  .en     (evict_addr_reg_en),
  .d      (make_addr_1),
  .q      (evict_addr_reg_out)
  );

  // memreq_addr_mux
  logic [31:0] memreq_addr_mux_out;
  vc_Mux2 #(32) memreq_addr_mux(
  .in1  (evict_addr_reg_out),
  .in0  (make_addr_0),
  .sel  (memreq_addr_mux_sel),
  .out  (memreq_addr_mux_out)
  );

  
  // read_data_zero_mux
  logic [127:0] read_data_zero_mux_out;
  vc_Mux2 #(128) read_data_zero_mux(
  .in1  (data_array_read_out),
  .in0  (128'h0),
  .sel  (read_data_zero_mux_sel), 
  .out  (read_data_zero_mux_out)
  );

  // read_data_reg
  logic [127:0] read_data_reg_out;
  vc_EnResetReg #(128,0) read_data_reg(
  .clk    (clk),
  .reset  (reset),
  .en     (read_data_reg_en),
  .d      (read_data_zero_mux_out),
  .q      (read_data_reg_out)
  );

  // 4-1 mux for read data
  logic [31:0] read_data_mux_out;
  vc_Mux4 #(32) read_data_mux(
  .in3  (read_data_reg_out[127:96]),
  .in2  (read_data_reg_out[95:64]),
  .in1  (read_data_reg_out[63:32]),
  .in0  (read_data_reg_out[31:0]),
  .sel  (cachereq_addr_word_offset),
  .out  (read_data_mux_out)
  );


  // Address Mapping

  logic  [1:0] cachereq_addr_byte_offset;
  logic  [1:0] cachereq_addr_word_offset;
  logic  [3:0] cachereq_addr_index;
  logic [23:0] cachereq_addr_tag;
  logic  [1:0] cachereq_addr_bank;

  generate
    if ( p_num_banks == 1 ) begin
      assign cachereq_addr_byte_offset = cachereq_addr[1:0];
      assign cachereq_addr_word_offset = cachereq_addr[3:2];
      assign cachereq_addr_index       = cachereq_addr[7:4];
      assign cachereq_addr_tag         = cachereq_addr[31:8];
    end
    else if ( p_num_banks == 4 ) begin
      // handle address mapping for four banks
      assign cachereq_addr_byte_offset = cachereq_addr[1:0];
      assign cachereq_addr_word_offset = cachereq_addr[3:2];
      assign cachereq_addr_bank        = cachereq_addr[5:4];
      assign cachereq_addr_index       = cachereq_addr[9:6];
      assign cachereq_addr_tag         = cachereq_addr[31:10];
    end
  endgenerate

  // Replicate cachereq_data

  logic [127:0] cachereq_data_replicated;

  lab3_mem_ReplUnit repl_unit
  (
    .in_ (cachereq_data_reg_out),
    .out (cachereq_data_replicated)
  );

  // Write byte enable decoder

  logic [15:0] wben_decoder_out;

  lab3_mem_WbenDecoder wben_decoder
  (
    .in_ (cachereq_addr_word_offset),
    .out (wben_decoder_out)
  );

  // Tag array (16 tags, 24 bits/tag)

  logic [23:0] tag_array_read_out;

  vc_CombinationalBitSRAM_1rw  #(
    .p_data_nbits  (24),
    .p_num_entries (16)
  )
  tag_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (tag_array_read_out),
    .write_en      (tag_array_wen),
    .read_en       (tag_array_ren),
    .write_addr    (cachereq_addr_index),
    .write_data    (cachereq_addr_tag)
  );

  // Data array (16 cacheslines, 128 bits/cacheline)

  logic [127:0] data_array_read_out;

  vc_CombinationalSRAM_1rw #(128,16) data_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (data_array_read_out),
    .write_en      (data_array_wen),
    .read_en       (data_array_ren),
    .write_byte_en (wben_mux_out),
    .write_addr    (cachereq_addr_index),
    .write_data    (write_data_mux_out)
  );

  // proc2cache_reqstream_msg

  assign proc2cache_respstream_msg.type_  = cachereq_type;
  assign proc2cache_respstream_msg.opaque = cachereq_opaque_reg_out;
  always_comb begin
    case (hit)
      2'b00: proc2cache_respstream_msg.test = 2'b00;
      2'b01: ;
      2'b10: proc2cache_respstream_msg.test = proc2cache_respstream_msg.test ^ 2'b01; 
      default: proc2cache_respstream_msg.test = 2'b00;
    endcase
  end
  assign proc2cache_respstream_msg.len    = 2'b0;
  assign proc2cache_respstream_msg.data = read_data_mux_out;

  // cache2mem_reqstream_msg
  assign cache2mem_reqstream_msg.data = read_data_reg_out;
  assign cache2mem_reqstream_msg.type_ = memreq_type;
  assign cache2mem_reqstream_msg.opaque = 8'b0;
  assign cache2mem_reqstream_msg.len = 4'b0;
  assign cache2mem_reqstream_msg.addr = memreq_addr_mux_out;

endmodule

`endif
