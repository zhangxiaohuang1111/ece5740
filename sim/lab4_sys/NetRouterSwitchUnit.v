//========================================================================
// Network Router Switch Unit
//========================================================================

`ifndef LAB4_SYS_NET_ROUTER_SWITCH_UNIT_V
`define LAB4_SYS_NET_ROUTER_SWITCH_UNIT_V

`include "vc/net-msgs.v"
`include "vc/trace.v"

module lab4_sys_NetRouterSwitchUnit
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Input streams

  input  logic [p_msg_nbits-1:0] istream_msg [3],
  input  logic                   istream_val [3],
  output logic                   istream_rdy [3],

  // Output stream

  output logic [p_msg_nbits-1:0] ostream_msg,
  output logic                   ostream_val,
  input  logic                   ostream_rdy
);

  // round-robin arbitration logic
  logic [1:0] last_served; // Tracks the last served input
  logic [1:0] selected_input;

  always_ff @( posedge clk ) begin
    if ( reset )
      last_served <= 0;
    else if ( ostream_val && ostream_rdy )
      last_served <= selected_input;
  end

  always_comb begin

    // Default outputs
    selected_input = 0;
    istream_rdy[0] = 0;
    istream_rdy[1] = 0;
    istream_rdy[2] = 0;
    ostream_val    = 0;
    ostream_msg    = 0;

    // Round-robin arbitration logic
    case ( last_served )
      2'd0: begin
        if ( istream_val[1] ) begin
          selected_input = 1;
          istream_rdy[1] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[1];
        end else if ( istream_val[2] ) begin
          selected_input = 2;
          istream_rdy[2] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[2];
        end else if ( istream_val[0] ) begin
          selected_input = 0;
          istream_rdy[0] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[0];
        end
      end
      2'd1: begin
        if ( istream_val[2] ) begin
          selected_input = 2;
          istream_rdy[2] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[2];
        end else if ( istream_val[0] ) begin
          selected_input = 0;
          istream_rdy[0] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[0];
        end else if ( istream_val[1] ) begin
          selected_input = 1;
          istream_rdy[1] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[1];
        end
      end
      2'd2: begin
        if ( istream_val[0] ) begin
          selected_input = 0;
          istream_rdy[0] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[0];
        end else if ( istream_val[1] ) begin
          selected_input = 1;
          istream_rdy[1] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[1];
        end else if ( istream_val[2] ) begin
          selected_input = 2;
          istream_rdy[2] = ostream_rdy;
          ostream_val    = 1;
          ostream_msg    = istream_msg[2];
        end
      end
       default : begin
        selected_input = 0;
        istream_rdy[0] = 0;
        istream_rdy[1] = 0;
        istream_rdy[2] = 0;
        ostream_val    = 0;
        ostream_msg    = 0;
      end
    endcase
  end

// discussion


//   logic [1:0] selected_input;

//   always_comb begin

//     selected_input = 0;
//     istream_rdy[0] = 0;
//     istream_rdy[1] = 0;
//     istream_rdy[2] = 0;
//     ostream_val    = 0;
//     ostream_msg    = 0;

//     if ( istream_val[1] ) begin
//   selected_input = 1;
//   istream_rdy[1] = ostream_rdy;
//   ostream_val    = 1;
//   ostream_msg    = istream_msg[1];
// end
// else if ( istream_val[2] ) begin
//   selected_input = 2;
//   istream_rdy[2] = ostream_rdy;
//   ostream_val    = 1;
//   ostream_msg    = istream_msg[2];
// end
// else if ( istream_val[0] ) begin
//   selected_input = 0;
//   istream_rdy[0] = ostream_rdy;
//   ostream_val    = 1;
//   ostream_msg    = istream_msg[0];
// end
//   end

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  integer num_reqs = 0;

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    num_reqs = istream_val[0] + istream_val[1] + istream_val[2];

    case ( num_reqs )
      0: vc_trace.append_str( trace_str, " " );
      1: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      3: vc_trace.append_str( trace_str, "#" );
    endcase

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_SWITCH_UNIT_V */
