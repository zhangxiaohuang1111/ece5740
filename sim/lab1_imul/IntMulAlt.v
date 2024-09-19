//=========================================================================
// Integer Multiplier Variable-Latency Implementation
//=========================================================================

`ifndef LAB1_IMUL_INT_MUL_ALT_V
`define LAB1_IMUL_INT_MUL_ALT_V

`include "vc/muxes.v"
`include "vc/arithmetic.v"
`include "vc/counters.v"
`include "vc/regs.v"
`include "vc/trace.v"

//=========================================================================
// Modified Unit Declearation
//=========================================================================

// // Complex right shifter used on b
// module ModifiedShifter_b
// #(
//   parameter p_nbits = 1
// )(
//   input  logic       [p_nbits-1:0] in,
//   input  logic       [$clog2(p_nbits+1)-1:0] max_shift,
//   output logic       [p_nbits-1:0] out,
//   output logic       [$clog2(p_nbits+1)-1:0] shift_num      // How many bits we shift
// );
//   logic [p_nbits-1:0] temp;
//   logic [$clog2(p_nbits+1)-1:0] shift_count;

//   integer i;
//   always_comb begin
//     temp = '0;
//     shift_count = '0;
    
//     if (in[0] == 0) begin  // shiftmode 1
//       temp = in;
//       shift_count = 0;

//       for (i = 0; (i < max_shift) && (temp[0] == 0); i = i + 1) begin
//         temp = temp >> 1;
//         shift_count = shift_count + 1;
//       end
//       out = temp;
//       shift_num = shift_count;
//     end else begin               // shiftmode 0
//       out = in >> 1;
//       shift_num = 1;
//     end
//   end
// endmodule

// Complex right shifter used on b
module ModifiedShifter_b
#(
  parameter p_nbits = 1
)(
  input  logic       [p_nbits-1:0] in,
  input  logic       [$clog2(p_nbits+1)-1:0] max_shift,
  output logic       [p_nbits-1:0] out,
  output logic       [$clog2(p_nbits+1)-1:0] shift_num      // How many bits we shift
);
  logic [p_nbits-1:0] temp;
  logic [$clog2(p_nbits+1)-1:0] shift_count;

  always_comb begin
    shift_num = 0;
    
    // // Code store for another design strategy
    // if (in[0] == 0) begin  // shiftmode 1

    //   if (temp[0] == 0 && shift_count < max_shift) begin // 1
    //     temp = temp >> 1;
    //     shift_count = shift_count + 1;

    //     if (temp[0] == 0 && shift_count < max_shift) begin // 2
    //       temp = temp >> 1;
    //       shift_count = shift_count + 1;

    //       if (temp[0] == 0 && shift_count < max_shift) begin // 3
    //         temp = temp >> 1;
    //         shift_count = shift_count + 1;

    //         if (temp[0] == 0 && shift_count < max_shift) begin // 4
    //           temp = temp >> 1;
    //           shift_count = shift_count + 1;

    //           if (temp[0] == 0 && shift_count < max_shift) begin // 5
    //             temp = temp >> 1;
    //             shift_count = shift_count + 1;

    //             if (temp[0] == 0 && shift_count < max_shift) begin // 6
    //               temp = temp >> 1;
    //               shift_count = shift_count + 1;

    //             end
    //           end
    //         end
    //       end
    //     end
    //   end

    //   out = temp;
    //   shift_num = shift_count;
      
    // end else begin  // shiftmode 0
    //   out = in >> 1;
    //   shift_num = 1;
    // end 
    
    if (in == 32'h80000000 && shift_count < max_shift) begin
      out = in >> 31;
      shift_num = 31;
    end else if (in == 32'h40000000 && shift_count < max_shift) begin
      out = in >> 30;
      shift_num = 30;
    end else if (in == 32'h20000000 && shift_count < max_shift) begin 
      out = in >> 29;
      shift_num = 29;
    end else if (in == 32'h10000000 && shift_count < max_shift) begin 
      out = in >> 28;
      shift_num = 28;
    end else if (in == 32'h08000000 && shift_count < max_shift) begin 
      out = in >> 27;
      shift_num = 27;
    end else if (in == 32'h04000000 && shift_count < max_shift) begin 
      out = in >> 26;
      shift_num = 26;
    end else if (in == 32'h02000000 && shift_count < max_shift) begin 
      out = in >> 25;
      shift_num = 25;
    end else if (in == 32'h01000000 && shift_count < max_shift) begin 
      out = in >> 24;
      shift_num = 24;
    end else if (in == 32'h00800000 && shift_count < max_shift) begin 
      out = in >> 23;
      shift_num = 23;
    end else if (in == 32'h00400000 && shift_count < max_shift) begin 
      out = in >> 22;
      shift_num = 22;
    end else if (in == 32'h00200000 && shift_count < max_shift) begin 
      out = in >> 21;
      shift_num = 21;
    end else if (in == 32'h00100000 && shift_count < max_shift) begin 
      out = in >> 20;
      shift_num = 20;
    end else if (in == 32'h00080000 && shift_count < max_shift) begin 
      out = in >> 19;
      shift_num = 19;
    end else if (in == 32'h00040000 && shift_count < max_shift) begin 
      out = in >> 18;
      shift_num = 18;
    end else if (in == 32'h00020000 && shift_count < max_shift) begin 
      out = in >> 17;
      shift_num = 17;
    end else if (in == 32'h00010000 && shift_count < max_shift) begin 
      out = in >> 16;
      shift_num = 16;
    end else if (in == 32'h00008000 && shift_count < max_shift) begin 
      out = in >> 15;
      shift_num = 15;
    end else if (in == 32'h00004000 && shift_count < max_shift) begin 
      out = in >> 14;
      shift_num = 14;
    end else if (in == 32'h00002000 && shift_count < max_shift) begin 
      out = in >> 13;
      shift_num = 13;
    end else if (in == 32'h00001000 && shift_count < max_shift) begin 
      out = in >> 12;
      shift_num = 12;
    end else if (in == 32'h00000800 && shift_count < max_shift) begin 
      out = in >> 11;
      shift_num = 11;
    end else if (in == 32'h00000400 && shift_count < max_shift) begin 
      out = in >> 10;
      shift_num = 10;
    end else if (in == 32'h00000200 && shift_count < max_shift) begin 
      out = in >> 9;
      shift_num = 9;
    end else if (in == 32'h00000100 && shift_count < max_shift) begin 
      out = in >> 8;
      shift_num = 8;
    end else if (in == 32'h00000080 && shift_count < max_shift) begin 
      out = in >> 7;
      shift_num = 7;
    end else if (in == 32'h00000040 && shift_count < max_shift) begin 
      out = in >> 6;
      shift_num = 6;
    end else if (in == 32'h00000020 && shift_count < max_shift) begin 
      out = in >> 5;
      shift_num = 5;
    end else if (in == 32'h00000010 && shift_count < max_shift) begin 
      out = in >> 4;
      shift_num = 4;
    end else if (in == 32'h00000008 && shift_count < max_shift) begin 
      out = in >> 3;
      shift_num = 3;
    end else if (in == 32'h00000004 && shift_count < max_shift) begin 
      out = in >> 2;
      shift_num = 2;
    end else if (in == 32'h00000002 && shift_count < max_shift) begin 
      out = in >> 1;
      shift_num = 1;
    end else begin
      out = in >> 1; // Only shift
      shift_num = 1;
    end
  end
endmodule


// Complex left shifter used on a that could shift multiple bits
// module ModifiedShifter_a
// #(
//   parameter p_nbits = 1
// )(
//   input  logic       [p_nbits-1:0] in,
//   input  logic       [$clog2(p_nbits+1)-1:0] shift_num,
//   output logic       [p_nbits-1:0] out
// );

//   assign out = ( in << shift_num );
// endmodule


// Counter in the vc folder with modification of add more than 1
module ModifiedCounter
#(
  parameter p_count_nbits       = 3,
  parameter p_count_clear_value = 0,
  parameter p_count_max_value   = 4
)(
  input  logic                     clk,
  input  logic                     reset,

  // Operations

  input  logic                     clear,
  input  logic                     increment,
  input  logic                     decrement,

  // Input

  input logic  [$clog2(p_count_nbits+1)-1:0] add_mul,

  // Outputs

  output logic [p_count_nbits-1:0] count,
  output logic                     count_is_zero,
  output logic                     count_is_max,
  output logic [p_count_nbits-1:0] max_shift

);

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------

  logic [p_count_nbits-1:0] count_next;

  vc_ResetReg#( p_count_nbits, p_count_clear_value ) count_reg
  (
    .clk   (clk),
    .reset (reset),
    .d     (count_next),
    .q     (count)
  );

  //----------------------------------------------------------------------
  // Combinational Logic
  //----------------------------------------------------------------------

  logic do_mul_increment;
  assign do_mul_increment = do_increment && (add_mul != 1);

  logic do_increment;
  assign do_increment = ( increment && (count < p_count_max_value) );

  logic do_decrement;
  assign do_decrement = ( decrement && (count > 0) );

  assign count_next
    = clear        ? (p_count_clear_value)
    : do_mul_increment ? (count + add_mul)
    : do_increment ? (count + 1)
    : do_decrement ? (count - 1)
    : count;

  assign count_is_zero = (count == 0);
  assign count_is_max  = (count == p_count_max_value);
  assign max_shift = 32 - count;  // Signal send to b shifter

endmodule



//=========================================================================
// Data Path
//=========================================================================
module lab1_imul_IntMulBaseDpath
(
  input  logic        clk,
  input  logic        reset,

  // Data signals
  input  logic [63:0] istream_msg,
  output logic [31:0] ostream_msg,

  // Control signals
  input  logic        a_reg_en,   // Enable for A register
  input  logic        b_reg_en,   // Enable for B register
  input  logic        result_reg_en,  // Enable for result register
  input  logic        a_mux_sel,  // Sel for mux in front of A reg
  input  logic        b_mux_sel,  // sel for mux in front of B reg
  input  logic        result_mux_sel,  // sel for mux in front of result reg
  input  logic        add_mux_sel,  // sel for mux in front of adder
  input  logic        counter_clear,  // Clear for counter

  // Status signals
  output logic       is_b0_one,  // Output of one comparator
  output logic       is_counter_max // Output of counter comparator
);

 localparam c_nbits = 32;


  // Split out the a and b operands
  logic [c_nbits-1:0] istream_msg_a;
  assign istream_msg_a = istream_msg[63:32];

  logic [c_nbits-1:0] istream_msg_b;
  assign istream_msg_b = istream_msg[31:0];


  // A Mux
  logic [c_nbits-1:0] left_shift_out;
  logic [c_nbits-1:0] a_mux_out;

  vc_Mux2#(c_nbits) a_mux
  ( 
    .sel   (a_mux_sel),
    .in0   (istream_msg_a),
    .in1   (left_shift_out),
    .out   (a_mux_out)
  ); // 0=id, 1=left shift


  // A register
  logic [c_nbits-1:0] a_reg_out;

  vc_EnReg#(c_nbits) a_reg
  (
    .clk   (clk),
    .reset (reset),
    .en    (a_reg_en),
    .d     (a_mux_out),
    .q     (a_reg_out)
  );


  // B Mux
  logic [c_nbits-1:0] b_mux_out;
  logic [c_nbits-1:0] right_shift_out;

  vc_Mux2#(c_nbits) b_mux // 0=id, 1=right shift
  (
    .sel   (b_mux_sel),
    .in0   (istream_msg_b),
    .in1   (right_shift_out),
    .out   (b_mux_out)
  );


  // B register
  logic [c_nbits-1:0] b_reg_out;
  vc_EnReg#(c_nbits) b_reg
  (
    .clk   (clk),
    .reset (reset),
    .en    (b_reg_en),
    .d     (b_mux_out),
    .q     (b_reg_out)
  );


  // add Mux 
  logic [c_nbits-1:0] add_mux_out;

  vc_Mux2#(c_nbits) add_mux //0=adder, 1=result
  (
    .sel   (add_mux_sel),
    .in0   (adder_out),
    .in1   (result_reg_out),
    .out   (add_mux_out)
  );


  // result Mux
  logic [c_nbits-1:0] result_mux_out;
  vc_Mux2#(c_nbits) result_mux //0=id,1=add_mux_out
  (
    .sel   (result_mux_sel),
    .in0   (32'd0),
    .in1   (add_mux_out),
    .out   (result_mux_out)
  );


  // result register
  logic [c_nbits-1:0] result_reg_out;

  vc_EnReg#(c_nbits) result_reg
  (
    .clk   (clk),
    .reset (reset),
    .en    (result_reg_en),
    .d     (result_mux_out),
    .q     (result_reg_out)
  );

  logic [$clog2(c_nbits+1)-1:0] shift_num;
  logic [$clog2(c_nbits+1)-1:0] max_shift;


  //b right shift
  ModifiedShifter_b#(c_nbits) right_shifter
  (
    .in    (b_reg_out),
    .max_shift(max_shift),
    .out   (right_shift_out),
    .shift_num(shift_num)
  );


  //a left shift
  vc_LeftLogicalShifter#(c_nbits, $clog2(c_nbits+1)) left_shifter
  (
    .in    (a_reg_out),
    .shamt(shift_num),
    .out   (left_shift_out)
  );


  //counter
  logic [c_nbits-1:0] counter_out;
  logic is_counter_zero;

  ModifiedCounter#(32, 0, 32) counter
  (
    .clk (clk),
    .reset (reset),
    .clear (counter_clear),
    .increment (1'b1),
    .decrement (1'b0),
    .add_mul(shift_num),
    .count (counter_out),
    .count_is_zero (is_counter_zero),
    .count_is_max (is_counter_max),
    .max_shift(max_shift)
  );


  //simple adder
  logic [c_nbits-1:0] adder_out;
  vc_SimpleAdder#(c_nbits) adder
  (
    .in0 (a_reg_out),
    .in1 (result_reg_out),
    .out (adder_out)
  );

  
  //comparators
  vc_EqComparator#(1) b0_one
  (
    .in0 (b_reg_out[0]),
    .in1 (1'b1),
    .out (is_b0_one)
  );

  // Connect to output port
  assign ostream_msg = result_reg_out;

endmodule



//=========================================================================
// Control Unit
//=========================================================================

module lab1_imul_IntMulBaseCtl
(
  input  logic        clk,
  input  logic        reset,

  // Dataflow signals
  input  logic        istream_val,
  output logic        istream_rdy,
  output logic        ostream_val,
  input  logic        ostream_rdy,

  // Control signals
  output logic        a_reg_en,   // Enable for A register
  output logic        b_reg_en,   // Enable for B register
  output logic        result_reg_en,  // Enable for result register
  output logic        a_mux_sel,  // Sel for mux in front of A reg
  output logic        b_mux_sel,  // sel for mux in front of B reg
  output logic        result_mux_sel,  // sel for mux in front of result reg
  output logic        add_mux_sel,  // sel for mux in front of adder
  output logic        counter_clear,  // Clear for counter

  // Data signals
  input  logic        is_b0_one,  // Output of one comparator
  input  logic        is_counter_max // Output of counter
);

  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------
  
  localparam STATE_IDLE = 2'd0;
  localparam STATE_CALC = 2'd1;
  localparam STATE_DONE = 2'd2;

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------
  
  logic [1:0] state_reg;
  logic [1:0] state_next;

    always_ff @( posedge clk ) begin
    if ( reset ) begin
      state_reg <= STATE_IDLE;
    end
    else begin
      state_reg <= state_next;
    end
  end

  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------
  
  logic req_go;
  logic resp_go;
  logic is_calc_done;

  assign req_go       = istream_val && istream_rdy;
  assign resp_go      = ostream_val && ostream_rdy;
  assign is_calc_done = is_counter_max;

  always_comb begin
    state_next = state_reg;
    case ( state_reg )
      STATE_IDLE: if ( req_go    )    state_next = STATE_CALC;
      STATE_CALC: if ( is_calc_done ) state_next = STATE_DONE;
      STATE_DONE: if ( resp_go   )    state_next = STATE_IDLE;
      default:    state_next = 'x;
    endcase
  end

//----------------------------------------------------------------------
// State Outputs
//----------------------------------------------------------------------

  localparam a_x       = 1'dx;
  localparam a_ld      = 1'd0;
  localparam a_shift   = 1'd1;

  localparam b_x       = 1'dx;
  localparam b_ld      = 1'd0;
  localparam b_shift   = 1'd1;

  localparam result_x  = 1'dx;
  localparam result_clear = 1'd0;
  localparam result_add= 1'd1;

  localparam add_x        = 1'dx;
  localparam add_mux      = 1'd0; //add mux out
  localparam add_result   = 1'd1; //result reg out

  function automatic void cs
  (
    input logic       cs_istream_rdy,
    input logic       cs_ostream_val,
    input logic       cs_a_mux_sel,
    input logic       cs_a_reg_en,
    input logic       cs_b_mux_sel,
    input logic       cs_b_reg_en,
    input logic       cs_result_mux_sel,
    input logic       cs_result_reg_en,
    input logic       cs_add_mux_sel,
    input logic       cs_counter_clear
  );
  begin
    istream_rdy   = cs_istream_rdy;
    ostream_val   = cs_ostream_val;
    a_reg_en      = cs_a_reg_en;
    b_reg_en      = cs_b_reg_en;
    a_mux_sel     = cs_a_mux_sel;
    b_mux_sel     = cs_b_mux_sel;
    result_mux_sel= cs_result_mux_sel;
    result_reg_en = cs_result_reg_en;
    add_mux_sel   = cs_add_mux_sel;
    counter_clear = cs_counter_clear;
  end
  endfunction
  // Labels for Mealy transistions

  logic do_add_shift;
  logic do_shift;

  assign do_add_shift = is_b0_one&&!is_counter_max;
  assign do_shift  = (~is_b0_one)&&!is_counter_max;

  // Set outputs using a control signal "table"

  always_comb begin
  //cs(is_istream_rdy, is_ostream_val, a_mux_sel, a_reg_en, b_mux_sel, b_reg_en, result_mux_sel, result_reg_en, add_mux_sel, counter_clear);
    cs( 0, 0, a_x, 0, b_x, 0,result_x, 0, add_x, 0);
    case ( state_reg )
  //cs(istream_rdy, ostream_val, a_mux_sel, a_reg_en, b_mux_sel, b_reg_en, result_mux_sel, result_reg_en, add_mux_sel, counter_clear);
      STATE_IDLE:                     cs( 1,   0,   a_ld,   1, b_ld,   1, result_clear,  1, add_x,      1);
      STATE_CALC: if ( do_add_shift ) cs( 0,   0,   a_shift,1, b_shift,1, result_add,    1, add_mux,    0);
             else if ( do_shift  )    cs( 0,   0,   a_shift,1, b_shift,1, result_add,    0, add_result, 0);
      STATE_DONE:                     cs( 0,   1,   a_x,    0, b_x,    0, result_x,      0, add_x,      0);
      default                         cs('x,  'x,   a_x,   'x, b_x,   'x, result_x,     'x, add_x,     'x);

    endcase

  end
endmodule





















//=========================================================================
// Integer Multiplier Variable-Latency Implementation
//=========================================================================

module lab1_imul_IntMulAlt
(
  input  logic        clk,
  input  logic        reset,

  input  logic        istream_val,
  output logic        istream_rdy,
  input  logic [63:0] istream_msg,

  output logic        ostream_val,
  input  logic        ostream_rdy,
  output logic [31:0] ostream_msg
);

  // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Instantiate datapath and control models here and then connect them
  // together.
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  //----------------------------------------------------------------------
  // Connect Control Unit and Datapath
  //----------------------------------------------------------------------
  
  // Control signals
  
  logic        a_reg_en;
  logic        b_reg_en;
  logic        a_mux_sel;
  logic        b_mux_sel;
  logic        result_mux_sel;
  logic        add_mux_sel;
  logic        counter_clear;
  logic        result_reg_en;
  
  // Data signals
  logic        is_b0_one;
  logic        is_counter_max;
  
  // Control unit
  
  lab1_imul_IntMulBaseCtl ctrl
  (
    .*
  );
  
  // Datapath
  
  lab1_imul_IntMulBaseDpath dpath
  (
    .*
  );
  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    $sformat( str, "%x", istream_msg );
    vc_trace.append_val_rdy_str( trace_str, istream_val, istream_rdy, str );

    vc_trace.append_str( trace_str, "(" );

    // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Add additional line tracing using the helper tasks for
    // internal state including the current FSM state.
    // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    vc_trace.append_str( trace_str, ")" );

    $sformat( str, "%x", ostream_msg );
    vc_trace.append_val_rdy_str( trace_str, ostream_val, ostream_rdy, str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* LAB1_IMUL_INT_MUL_ALT_V */

