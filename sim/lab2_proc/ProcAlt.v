//=========================================================================
// 5-Stage Fully Bypassed Pipelined Processor
//=========================================================================

`ifndef LAB2_PROC_PROC_ALT_V
`define LAB2_PROC_PROC_ALT_V

`include "vc/mem-msgs.v"
`include "vc/queues.v"
`include "vc/trace.v"

//''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// Include components here
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab2_proc_ProcAlt
#(
  parameter p_num_cores = 1
)
(
  input  logic         clk,
  input  logic         reset,

  // From mngr streaming port

  input  logic [31:0]  mngr2proc_msg,
  input  logic         mngr2proc_val,
  output logic         mngr2proc_rdy,

  // To mngr streaming port

  output logic [31:0]  proc2mngr_msg,
  output logic         proc2mngr_val,
  input  logic         proc2mngr_rdy,

  // Instruction Memory Request Port

  output mem_req_4B_t  imem_reqstream_msg,
  output logic         imem_reqstream_val,
  input  logic         imem_reqstream_rdy,

  // Instruction Memory Response Port

  input  mem_resp_4B_t imem_respstream_msg,
  input  logic         imem_respstream_val,
  output logic         imem_respstream_rdy,

  // Data Memory Request Port

  output mem_req_4B_t  dmem_reqstream_msg,
  output logic         dmem_reqstream_val,
  input  logic         dmem_reqstream_rdy,

  // Data Memory Response Port

  input  mem_resp_4B_t dmem_respstream_msg,
  input  logic         dmem_respstream_val,
  output logic         dmem_respstream_rdy,

  // stats output; core_id is an input port rather than a parameter so
  // that the module only needs to be compiled once. If it were a
  // parameter, each core would be compiled separately.

  input  logic [31:0]  core_id,
  output logic         commit_inst,
  output logic         stats_en
);

  //----------------------------------------------------------------------
  // Instruction Memory Request Bypass Queue
  //----------------------------------------------------------------------

  logic [1:0]  imem_queue_num_free_entries;
  mem_req_4B_t imem_reqstream_enq_msg;
  logic        imem_reqstream_enq_val;
  logic        imem_reqstream_enq_rdy;

  logic [31:0] imem_reqstream_enq_msg_addr;

  assign imem_reqstream_enq_msg.type_  = `VC_MEM_REQ_MSG_TYPE_READ;
  assign imem_reqstream_enq_msg.opaque = 8'b0;
  assign imem_reqstream_enq_msg.addr   = imem_reqstream_enq_msg_addr;
  assign imem_reqstream_enq_msg.len    = 2'd0;
  assign imem_reqstream_enq_msg.data   = 32'bx;

  vc_Queue#(`VC_QUEUE_BYPASS,$bits(mem_req_4B_t),2) imem_queue
  (
    .clk     (clk),
    .reset   (reset),
    .num_free_entries(imem_queue_num_free_entries),

    .enq_msg (imem_reqstream_enq_msg),
    .enq_val (imem_reqstream_enq_val),
    .enq_rdy (imem_reqstream_enq_rdy),

    .deq_msg (imem_reqstream_msg),
    .deq_val (imem_reqstream_val),
    .deq_rdy (imem_reqstream_rdy)
  );

  //----------------------------------------------------------------------
  // Imem Drop Unit
  //----------------------------------------------------------------------

  logic         imem_respstream_drop;
  mem_resp_4B_t imem_respstream_drop_msg;
  logic         imem_respstream_drop_val;
  logic         imem_respstream_drop_rdy;

  lab2_proc_DropUnit #($bits(mem_resp_4B_t)) imem_respstream_drop_unit
  (
    .clk         (clk),
    .reset       (reset),

    .drop        (imem_respstream_drop),

    .istream_msg (imem_respstream_msg),
    .istream_val (imem_respstream_val),
    .istream_rdy (imem_respstream_rdy),

    .ostream_msg (imem_respstream_drop_msg),
    .ostream_val (imem_respstream_drop_val),
    .ostream_rdy (imem_respstream_drop_rdy)
  );

  //----------------------------------------------------------------------
  // Data Memory Request Bypass Queue
  //----------------------------------------------------------------------

  logic        dmem_queue_num_free_entries;
  mem_req_4B_t dmem_reqstream_enq_msg;
  logic        dmem_reqstream_enq_val;
  logic        dmem_reqstream_enq_rdy;

  logic [ 3:0] dmem_reqstream_enq_msg_type;
  logic [31:0] dmem_reqstream_enq_msg_addr;
  logic [31:0] dmem_reqstream_enq_msg_data;

  assign dmem_reqstream_enq_msg.type_  = dmem_reqstream_enq_msg_type;
  assign dmem_reqstream_enq_msg.opaque = 8'b0;
  assign dmem_reqstream_enq_msg.addr   = dmem_reqstream_enq_msg_addr;
  assign dmem_reqstream_enq_msg.len    = 2'd0;
  assign dmem_reqstream_enq_msg.data   = dmem_reqstream_enq_msg_data;

  vc_Queue#(`VC_QUEUE_BYPASS,$bits(mem_req_4B_t),1) dmem_queue
  (
    .clk     (clk),
    .reset   (reset),
    .num_free_entries(dmem_queue_num_free_entries),

    .enq_msg (dmem_reqstream_enq_msg),
    .enq_val (dmem_reqstream_enq_val),
    .enq_rdy (dmem_reqstream_enq_rdy),

    .deq_msg (dmem_reqstream_msg),
    .deq_val (dmem_reqstream_val),
    .deq_rdy (dmem_reqstream_rdy)
  );

  //----------------------------------------------------------------------
  // proc2mngr Bypass Queue
  //----------------------------------------------------------------------

  logic        proc2mngr_queue_num_free_entries;
  logic [31:0] proc2mngr_enq_msg;
  logic        proc2mngr_enq_val;
  logic        proc2mngr_enq_rdy;

  vc_Queue#(`VC_QUEUE_BYPASS,32,1) proc2mngr_queue
  (
    .clk     (clk),
    .reset   (reset),
    .num_free_entries(proc2mngr_queue_num_free_entries),

    .enq_msg (proc2mngr_enq_msg),
    .enq_val (proc2mngr_enq_val),
    .enq_rdy (proc2mngr_enq_rdy),

    .deq_msg (proc2mngr_msg),
    .deq_val (proc2mngr_val),
    .deq_rdy (proc2mngr_rdy)
  );

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Instantiate and connect components here
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //----------------------------------------------------------------------
  // Line tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  lab2_proc_tinyrv2_encoding_InstTasks tinyrv2();

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    if ( !ctrl.val_F )
      vc_trace.append_chars( trace_str, " ", 8 );
    else if ( ctrl.squash_F ) begin
      vc_trace.append_str( trace_str, "/" );
      vc_trace.append_chars( trace_str, " ", 8-1 );
    end else if ( ctrl.stall_F ) begin
      vc_trace.append_str( trace_str, "#" );
      vc_trace.append_chars( trace_str, " ", 8-1 );
    end else begin
      $sformat( str, "%x", dpath.pc_F );
      vc_trace.append_str( trace_str, str );
    end

    vc_trace.append_str( trace_str, "|" );

    if ( !ctrl.val_D )
      vc_trace.append_chars( trace_str, " ", 23 );
    else if ( ctrl.squash_D ) begin
      vc_trace.append_str( trace_str, "/" );
      vc_trace.append_chars( trace_str, " ", 23-1 );
    end else if ( ctrl.stall_D ) begin
      vc_trace.append_str( trace_str, "#" );
      vc_trace.append_chars( trace_str, " ", 23-1 );
    end else
      vc_trace.append_str( trace_str, { 3896'b0, tinyrv2.disasm( ctrl.inst_D ) } );

    vc_trace.append_str( trace_str, "|" );

    if ( !ctrl.val_X )
      vc_trace.append_chars( trace_str, " ", 4 );
    else if ( ctrl.stall_X ) begin
      vc_trace.append_str( trace_str, "#" );
      vc_trace.append_chars( trace_str, " ", 4-1 );
    end else
      vc_trace.append_str( trace_str, { 4064'b0, tinyrv2.disasm_tiny( ctrl.inst_X ) } );

    vc_trace.append_str( trace_str, "|" );

    if ( !ctrl.val_M )
      vc_trace.append_chars( trace_str, " ", 4 );
    else if ( ctrl.stall_M ) begin
      vc_trace.append_str( trace_str, "#" );
      vc_trace.append_chars( trace_str, " ", 4-1 );
    end else
      vc_trace.append_str( trace_str, { 4064'b0, tinyrv2.disasm_tiny( ctrl.inst_M ) } );

    vc_trace.append_str( trace_str, "|" );

    if ( !ctrl.val_W )
      vc_trace.append_chars( trace_str, " ", 4 );
    else if ( ctrl.stall_W ) begin
      vc_trace.append_str( trace_str, "#" );
      vc_trace.append_chars( trace_str, " ", 4-1 );
    end else
      vc_trace.append_str( trace_str, { 4064'b0, tinyrv2.disasm_tiny( ctrl.inst_W ) } );

  end
  `VC_TRACE_END

  // These trace modules are useful because they breakout all the
  // individual fields so you can see them in gtkwave

  vc_MemReqMsg4BTrace imem_reqstream_trace
  (
    .clk   (clk),
    .reset (reset),
    .val   (imem_reqstream_val),
    .rdy   (imem_reqstream_rdy),
    .msg   (imem_reqstream_msg)
  );

  vc_MemReqMsg4BTrace dmem_reqstream_trace
  (
    .clk   (clk),
    .reset (reset),
    .val   (dmem_reqstream_val),
    .rdy   (dmem_reqstream_rdy),
    .msg   (dmem_reqstream_msg)
  );

  vc_MemRespMsg4BTrace imem_respstream_trace
  (
    .clk   (clk),
    .reset (reset),
    .val   (imem_respstream_val),
    .rdy   (imem_respstream_rdy),
    .msg   (imem_respstream_msg)
  );

  vc_MemRespMsg4BTrace dmem_respstream_trace
  (
    .clk   (clk),
    .reset (reset),
    .val   (dmem_respstream_val),
    .rdy   (dmem_respstream_rdy),
    .msg   (dmem_respstream_msg)
  );

  `endif

endmodule

`endif

