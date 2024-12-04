//========================================================================
// Ring Network
//========================================================================

`ifndef LAB4_SYS_NET_V
`define LAB4_SYS_NET_V

`include "vc/net-msgs.v"
`include "vc/trace.v"
`include "vc/queues.v"

`include "lab4_sys/NetRouter.v"

module lab4_sys_Net
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Input streams

  input  logic [p_msg_nbits-1:0] istream_msg [4],
  input  logic                   istream_val [4],
  output logic                   istream_rdy [4],

  // Output streams

  output logic [p_msg_nbits-1:0] ostream_msg [4],
  output logic                   ostream_val [4],
  input  logic                   ostream_rdy [4]
);

  // Clockwise and couter-clockwise channels

  logic [p_msg_nbits-1:0] channels_cw_msg  [4];
  logic                   channels_cw_val  [4];
  logic                   channels_cw_rdy  [4];

  logic [p_msg_nbits-1:0] channels_ccw_msg [4];
  logic                   channels_ccw_val [4];
  logic                   channels_ccw_rdy [4];

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Implement ring network with four routers
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

logic [p_msg_nbits-1:0] istream_msg_r0 [3];
logic                   istream_val_r0 [3];
logic                   istream_rdy_r0 [3];
logic [p_msg_nbits-1:0] ostream_msg_r0 [3];
logic                   ostream_val_r0 [3];
logic                   ostream_rdy_r0 [3];

  // Router 0 Input Ports
  assign istream_msg_r0[0] = channels_cw_msg[3];
  assign istream_val_r0[0] = channels_cw_val[3];
  assign channels_cw_rdy[3] = istream_rdy_r0[0];

  assign istream_msg_r0[1] = channels_ccw_msg[0];    
  assign istream_val_r0[1] = channels_ccw_val[0];
  assign channels_ccw_rdy[0] = istream_rdy_r0[1];

  assign istream_msg_r0[2] = istream_msg[0];        
  assign istream_val_r0[2] = istream_val[0];
  assign istream_rdy[0] = istream_rdy_r0[2];

  // Router 0 Output Ports
  assign ostream_msg[0] = ostream_msg_r0[2];        
  assign ostream_val[0] = ostream_val_r0[2];
  assign ostream_rdy_r0[2] = ostream_rdy[0];

  assign channels_cw_msg[0] = ostream_msg_r0[1];    
  assign channels_cw_val[0] = ostream_val_r0[1];
  assign ostream_rdy_r0[1] = channels_cw_rdy[0];

  assign channels_ccw_msg[3] = ostream_msg_r0[0];   
  assign channels_ccw_val[3] = ostream_val_r0[0];
  assign ostream_rdy_r0[0] = channels_ccw_rdy[3];
  // Instantiate Router 0
  lab4_sys_NetRouter#(p_msg_nbits) router0 (
    .clk          (clk),
    .reset        (reset),
    .router_id    (2'b00),          // Router 0 ID
    .istream_msg  (istream_msg_r0),
    .istream_val  (istream_val_r0),
    .istream_rdy  (istream_rdy_r0),
    .ostream_msg  (ostream_msg_r0),
    .ostream_val  (ostream_val_r0),
    .ostream_rdy  (ostream_rdy_r0)
  );

logic [p_msg_nbits-1:0] istream_msg_r1 [3];
logic                   istream_val_r1 [3];
logic                   istream_rdy_r1 [3];
logic [p_msg_nbits-1:0] ostream_msg_r1 [3];
logic                   ostream_val_r1 [3];
logic                   ostream_rdy_r1 [3];
    // Router 1 Input Ports
  assign istream_msg_r1[0] = channels_cw_msg[0];
  assign istream_val_r1[0] = channels_cw_val[0];
  assign channels_cw_rdy[0] = istream_rdy_r1[0];

  assign istream_msg_r1[1] = channels_ccw_msg[1];
  assign istream_val_r1[1] = channels_ccw_val[1];
  assign channels_ccw_rdy[1] = istream_rdy_r1[1];

  assign istream_msg_r1[2] = istream_msg[1];
  assign istream_val_r1[2] = istream_val[1];
  assign istream_rdy[1] = istream_rdy_r1[2];

  // Router 1 Output Ports
  assign ostream_msg[1] = ostream_msg_r1[2];
  assign ostream_val[1] = ostream_val_r1[2];
  assign ostream_rdy_r1[2] = ostream_rdy[1];

  assign channels_cw_msg[1] = ostream_msg_r1[1];
  assign channels_cw_val[1] = ostream_val_r1[1];
  assign ostream_rdy_r1[1] = channels_cw_rdy[1];

  assign channels_ccw_msg[0] = ostream_msg_r1[0];
  assign channels_ccw_val[0] = ostream_val_r1[0];
  assign ostream_rdy_r1[0] = channels_ccw_rdy[0];

  // Instantiate Router 1
  lab4_sys_NetRouter#(p_msg_nbits) router1 (
    .clk          (clk),
    .reset        (reset),
    .router_id    (2'b01),          // Router 1 ID
    .istream_msg  (istream_msg_r1),
    .istream_val  (istream_val_r1),
    .istream_rdy  (istream_rdy_r1),
    .ostream_msg  (ostream_msg_r1),
    .ostream_val  (ostream_val_r1),
    .ostream_rdy  (ostream_rdy_r1)
  );
logic [p_msg_nbits-1:0] istream_msg_r2 [3];
logic                   istream_val_r2 [3];
logic                   istream_rdy_r2 [3];
logic [p_msg_nbits-1:0] ostream_msg_r2 [3];
logic                   ostream_val_r2 [3];
logic                   ostream_rdy_r2 [3];
    // Router 2 Input Ports
  assign istream_msg_r2[0] = channels_cw_msg[1];
  assign istream_val_r2[0] = channels_cw_val[1];
  assign channels_cw_rdy[1] = istream_rdy_r2[0];

  assign istream_msg_r2[1] = channels_ccw_msg[2];
  assign istream_val_r2[1] = channels_ccw_val[2];
  assign channels_ccw_rdy[2] = istream_rdy_r2[1];

  assign istream_msg_r2[2] = istream_msg[2];
  assign istream_val_r2[2] = istream_val[2];
  assign istream_rdy[2] = istream_rdy_r2[2];

  // Router 2 Output Ports
  assign ostream_msg[2] = ostream_msg_r2[2];
  assign ostream_val[2] = ostream_val_r2[2];
  assign ostream_rdy_r2[2] = ostream_rdy[2];

  assign channels_cw_msg[2] = ostream_msg_r2[1];
  assign channels_cw_val[2] = ostream_val_r2[1];
  assign ostream_rdy_r2[1] = channels_cw_rdy[2];

  assign channels_ccw_msg[1] = ostream_msg_r2[0];
  assign channels_ccw_val[1] = ostream_val_r2[0];
  assign ostream_rdy_r2[0] = channels_ccw_rdy[1];

  // Instantiate Router 2
  lab4_sys_NetRouter#(p_msg_nbits) router2 (
    .clk          (clk),
    .reset        (reset),
    .router_id    (2'b10),          // Router 2 ID
    .istream_msg  (istream_msg_r2),
    .istream_val  (istream_val_r2),
    .istream_rdy  (istream_rdy_r2),
    .ostream_msg  (ostream_msg_r2),
    .ostream_val  (ostream_val_r2),
    .ostream_rdy  (ostream_rdy_r2)
  );
logic [p_msg_nbits-1:0] istream_msg_r3 [3];
logic                   istream_val_r3 [3];
logic                   istream_rdy_r3 [3];
logic [p_msg_nbits-1:0] ostream_msg_r3 [3];
logic                   ostream_val_r3 [3];
logic                   ostream_rdy_r3 [3];
    // Router 3 Input Ports
  assign istream_msg_r3[0] = channels_cw_msg[2];
  assign istream_val_r3[0] = channels_cw_val[2];
  assign channels_cw_rdy[2] = istream_rdy_r3[0];

  assign istream_msg_r3[1] = channels_ccw_msg[3];
  assign istream_val_r3[1] = channels_ccw_val[3];
  assign channels_ccw_rdy[3] = istream_rdy_r3[1];

  assign istream_msg_r3[2] = istream_msg[3];
  assign istream_val_r3[2] = istream_val[3];
  assign istream_rdy[3] = istream_rdy_r3[2];

  // Router 3 Output Ports
  assign ostream_msg[3] = ostream_msg_r3[2];
  assign ostream_val[3] = ostream_val_r3[2];
  assign ostream_rdy_r3[2] = ostream_rdy[3];

  assign channels_cw_msg[3] = ostream_msg_r3[1];
  assign channels_cw_val[3] = ostream_val_r3[1];
  assign ostream_rdy_r3[1] = channels_cw_rdy[3];

  assign channels_ccw_msg[2] = ostream_msg_r3[0];
  assign channels_ccw_val[2] = ostream_val_r3[0];
  assign ostream_rdy_r3[0] = channels_ccw_rdy[2];

  // Instantiate Router 3
  lab4_sys_NetRouter#(p_msg_nbits) router3 (
    .clk          (clk),
    .reset        (reset),
    .router_id    (2'b11),          // Router 3 ID
    .istream_msg  (istream_msg_r3),
    .istream_val  (istream_val_r3),
    .istream_rdy  (istream_rdy_r3),
    .ostream_msg  (ostream_msg_r3),
    .ostream_val  (ostream_val_r3),
    .ostream_rdy  (ostream_rdy_r3)
  );
  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  // Generate for loop to instantiate trace modules

  genvar j;
  generate
  for ( j = 0; j < 4; j = j + 1 ) begin: CHANNEL_TRACE

    vc_NetMsgMiniTrace#(p_msg_nbits) cw_trace
    (
      .clk   (clk),
      .reset (reset),
      .msg   (channels_cw_msg[j]),
      .val   (channels_cw_val[j]),
      .rdy   (channels_cw_rdy[j])
    );

    vc_NetMsgMiniTrace#(p_msg_nbits) ccw_trace
    (
      .clk   (clk),
      .reset (reset),
      .msg   (channels_ccw_msg[j]),
      .val   (channels_ccw_val[j]),
      .rdy   (channels_ccw_rdy[j])
    );

  end
  endgenerate

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    // Line tracing for clockwise channels

    CHANNEL_TRACE[0].cw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[1].cw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[2].cw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[3].cw_trace.line_trace( trace_str );

    vc_trace.append_str( trace_str, "I" );

    // Line tracing for counter clockwise channels

    CHANNEL_TRACE[0].ccw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[1].ccw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[2].ccw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[3].ccw_trace.line_trace( trace_str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* LAB4_SYS_NET_V */
