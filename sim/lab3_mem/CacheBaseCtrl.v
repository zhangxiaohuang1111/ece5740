//=========================================================================
// Base Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_CACHE_BASE_CTRL_V
`define LAB3_MEM_CACHE_BASE_CTRL_V

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
`include "vc/regfiles.v"
`include "vc/mem-msgs.v"

module lab3_mem_CacheBaseCtrl
#(
  parameter p_num_banks = 1
)
(
  input  logic        clk,
  input  logic        reset,

  // Processor <-> Cache Interface

  input  logic        proc2cache_reqstream_val,
  output logic        proc2cache_reqstream_rdy,

  output logic        proc2cache_respstream_val,
  input  logic        proc2cache_respstream_rdy,

  // Cache <-> Memory Interface

  output logic        cache2mem_reqstream_val,
  input  logic        cache2mem_reqstream_rdy,

  input  logic        cache2mem_respstream_val,
  output logic        cache2mem_respstream_rdy,

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Define additional ports
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  // control signals (ctrl->dpath)

  output  logic          cachereq_reg_en,
  output  logic          memresp_reg_en,
  output  logic          write_data_mux_sel,
  output  logic          wben_mux_sel,
  output  logic          tag_array_wen,
  output  logic          tag_array_ren,
  output  logic          data_array_wen,
  output  logic          data_array_ren,
  output  logic          read_data_zero_mux_sel,
  output  logic          read_data_reg_en,
  output  logic          evict_addr_reg_en,
  output  logic          memreq_addr_mux_sel,
  output  logic [3:0]    cacheresp_type,
  output  logic [1:0]    hit,
  output  logic [3:0]    memreq_type,

  // status signals (dpath->ctrl)

  input logic  [3:0]     cachereq_type,
  input logic [31:0]     cachereq_addr,
  input logic            tag_match

);

  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------

  localparam STATE_IDLE              = 5'd0;
  localparam STATE_TAG_CHECK         = 5'd1;
  localparam STATE_INIT_DATA_ACCESS  = 5'd2;
  localparam STATE_READ_DATA_ACCESS  = 5'd3;
  localparam STATE_WRITE_DATA_ACCESS = 5'd4;
  localparam STATE_REFILL_REQUEST    = 5'd5;
  localparam STATE_REFILL_WAIT       = 5'd6;
  localparam STATE_REFILL_UPDATE     = 5'd7;
  localparam STATE_EVICT_PREPARE     = 5'd8;
  localparam STATE_EVICT_REQUEST     = 5'd9;
  localparam STATE_EVICT_WAIT        = 5'd10;
  localparam STATE_WAIT              = 5'd11;

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Impement control unit
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------

  always @( posedge clk ) begin
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

  logic is_read;
  logic is_write;
  logic is_init;

  assign is_read  = cachereq_type == `VC_MEM_REQ_MSG_TYPE_READ;
  assign is_write = cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE;
  assign is_init  = cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE_INIT;

  logic [4:0] state_reg;
  logic [4:0] state_next;

  always @(*) begin
  state_next = state_reg;
  case ( state_reg )

    // Initial idle state
    STATE_IDLE:
      if ( proc2cache_reqstream_val ) // When there’s a request from the processor, move to TAG_CHECK
        state_next = STATE_TAG_CHECK;
      else
        state_next = STATE_IDLE;        // Stay in idle state
    // TAG check state to determine hit or miss
    STATE_TAG_CHECK:
      if ( is_init )
          state_next = STATE_INIT_DATA_ACCESS;  // Initialization transaction, move to init data access
      else if ( tag_match&&is_read ) 
          state_next = STATE_READ_DATA_ACCESS;  // Read hit, move to read data state
      else if ( tag_match&&is_write ) 
          state_next = STATE_WRITE_DATA_ACCESS; // Write hit, move to write data state
      else if ( !tag_match&&is_valid ) 
          state_next = STATE_REFILL_REQUEST;    // Read miss, move to refill request stat
      else if ( !tag_match&&!is_valid )
          state_next = STATE_EVICT_PREPARE;     // Write miss, move to evict prepare state
    STATE_INIT_DATA_ACCESS:
      state_next = STATE_WAIT;                  // Initialization transaction, move to wait state
    STATE_READ_DATA_ACCESS:
      state_next = STATE_WAIT;                  // Read hit, move to wait state
    STATE_WRITE_DATA_ACCESS:
      state_next = STATE_WAIT;                  // Write hit, move to wait state
    STATE_EVICT_PREPARE:
      state_next = STATE_EVICT_REQUEST;         // Write miss, move to evict request state
    STATE_EVICT_REQUEST:
      if (cache2mem_reqstream_rdy)                // When there’s a request from the cache, move to evict wait state
        state_next = STATE_EVICT_WAIT;            // Write miss, move to evict wait state
      else if ( !cache2mem_reqstream_rdy )        // When there’s no request from the cache, stay in evict request state
        state_next = STATE_EVICT_REQUEST;
    STATE_EVICT_WAIT:
      if(cache2mem_respstream_val)             // When there’s a response from the cache, move to refill request state
        state_next = STATE_REFILL_REQUEST;        // Write miss, move to refill request state
      else if ( !cache2mem_respstream_val )    // When there’s no response from the cache, stay in evict wait state
        state_next = STATE_EVICT_WAIT;
    STATE_REFILL_REQUEST:
      if (cache2mem_reqstream_rdy)                // When there’s a request from the cache, move to refill wait state
        state_next = STATE_REFILL_WAIT;           // Read miss, move to refill wait state
      else if ( !cache2mem_reqstream_rdy )        // When there’s no request from the cache, stay in refill request state
        state_next = STATE_REFILL_REQUEST;
    STATE_REFILL_WAIT:
      if(cache2mem_respstream_val)             // When there’s a response from the cache, move to refill update state
        state_next = STATE_REFILL_UPDATE;         // Read miss, move to refill update state
      else if ( !cache2mem_respstream_val )    // When there’s no response from the cache, stay in refill wait state
        state_next = STATE_REFILL_WAIT;
    STATE_REFILL_UPDATE:
      if(is_read)                               // When there’s a read request, move to read data access state
        state_next = STATE_READ_DATA_ACCESS;
      else if (is_write)                        // When there’s a write request, move to write data access state
        state_next = STATE_WRITE_DATA_ACCESS;
      else
      state_next = STATE_WAIT;                  // Read miss, move to wait state
    STATE_WAIT:
      if(proc2cache_respstream_rdy)             // When there’s a response from the cache, move to idle state
        state_next = STATE_IDLE;
      else if ( !proc2cache_respstream_rdy )    // When there’s no response from the cache, stay in wait state
        state_next = STATE_WAIT;
    default:
      state_next = STATE_IDLE;

  endcase
end

  //----------------------------------------------------------------------
  // Valid/Dirty bits record
  //----------------------------------------------------------------------

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

  logic valid_bit_in;
  logic valid_bits_write_en;
  logic is_valid;

  vc_ResetRegfile_1r1w#(1,16) valid_bits
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_valid),
    .write_en   (valid_bits_write_en),
    .write_addr (cachereq_addr_index),
    .write_data (valid_bit_in)
  );

  //----------------------------------------------------------------------
  // State Outputs
  //----------------------------------------------------------------------

  task cs
  (
    input logic cs_cachereq_rdy,
    input logic cs_cacheresp_val,
    input logic cs_memreq_val,
    input logic cs_memresp_rdy,
    input logic cs_cachereq_reg_en,
    input logic cs_memresp_reg_en,
    input logic cs_write_data_mux_sel,
    input logic cs_wben_mux_sel,
    input logic cs_tag_array_wen,
    input logic cs_tag_array_ren,
    input logic cs_data_array_wen,
    input logic cs_data_array_ren,
    input logic cs_read_data_zero_mux_sel,
    input logic cs_read_data_reg_en,
    input logic cs_evict_addr_reg_en,
    input logic cs_memreq_addr_mux_sel,
    input logic [3:0] cs_cacheresp_type,
    input logic [1:0] cs_hit,
    input logic [3:0] cs_memreq_type,
    input logic cs_valid_bit_in,
    input logic cs_valid_bits_write_en

  );
  begin
    proc2cache_reqstream_rdy  = cs_cachereq_rdy;
    proc2cache_respstream_val = cs_cacheresp_val;
    cache2mem_reqstream_val   = cs_memreq_val;
    cache2mem_respstream_rdy  = cs_memresp_rdy;
    cachereq_reg_en           = cs_cachereq_reg_en;
    memresp_reg_en            = cs_memresp_reg_en;
    write_data_mux_sel        = cs_write_data_mux_sel;
    wben_mux_sel              = cs_wben_mux_sel;
    tag_array_wen             = cs_tag_array_wen;
    tag_array_ren             = cs_tag_array_ren;
    data_array_wen            = cs_data_array_wen;
    data_array_ren            = cs_data_array_ren;
    read_data_zero_mux_sel    = cs_read_data_zero_mux_sel;
    read_data_reg_en          = cs_read_data_reg_en;
    evict_addr_reg_en         = cs_evict_addr_reg_en;
    memreq_addr_mux_sel       = cs_memreq_addr_mux_sel;
    cacheresp_type            = cs_cacheresp_type;
    hit                       = cs_hit;
    memreq_type               = cs_memreq_type;
    valid_bit_in              = cs_valid_bit_in;
    valid_bits_write_en       = cs_valid_bits_write_en;
  end
  endtask

  // Set outputs using a control signal "table"
  always @(*) begin
                              cs( 0,   0,    0,    0,    0,    0,    0,    0,    0     );
    case ( state_reg )
      //                             cache cache cache tag   tag   data  data  valid valid
      //                             req   resp  req   array array array array bit   write
      //                             rdy   val   en    wen   ren   wen   ren   in    en

      STATE_IDLE:                  cs( 1,   0,    1,    0,    0,    0,    0,    0,    0     );
      STATE_TAG_CHECK:             cs( 0,   0,    0,    0,    1,    0,    0,    0,    0     );
      STATE_INIT_DATA_ACCESS:      cs( 0,   0,    0,    1,    0,    1,    0,    1,    1     );
      STATE_WAIT:                  cs( 0,   1,    0,    0,    0,    0,    0,    0,    0     );

      // ''' SECTION  ''''''''''''''''''''''''''''''''''''''''''''''''''''
      // Add outputs for TAG_CHECK, DATA_ACCESS, WAIT states
      // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

      default:                cs( 0,   0,    0,    0,    0,    0,    0,    0,    0     );

    endcase
  end

  // Hard code cache <-> memory interface val/rdy signals since we are
  // not using this interface yet

  assign cache2mem_reqstream_val  = 1'b0;
  assign cache2mem_respstream_rdy = 1'b1;
endmodule

`endif
