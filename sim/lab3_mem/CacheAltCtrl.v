//=========================================================================
// Alt Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_CACHE_ALT_CTRL_V
`define LAB3_MEM_CACHE_ALT_CTRL_V


//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
`include "vc/regfiles.v"
`include "vc/mem-msgs.v"

module lab3_mem_CacheAltCtrl
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
  output  logic          tag_array_0_wen,
  output  logic          tag_array_1_wen,
  output  logic          tag_array_ren,
  output  logic          data_array_0_wen,
  output  logic          data_array_1_wen,
  output  logic          data_array_ren,
  output  logic          read_data_zero_mux_sel,
  output  logic          read_data_reg_en,
  output  logic          evict_addr_reg_en,
  output  logic          memreq_addr_mux_sel,
  output  logic [1:0]    hit,
  output  logic [3:0]    memreq_type,
  output  logic          current_way,     // 1 bit current way indicator

  // status signals (dpath->ctrl)

  input logic   [3:0]   cachereq_type,
  input logic   [31:0]  cachereq_addr,
  input logic           tag_0_match,
  input logic           tag_1_match
);

  // logic [1:0] test;
  // always @(*) begin
  //   case (tag_match)
  //     1'b1: 
  //         test = 2'b1;
  //     1'b0:
  //         test = 2'b0;
  //   endcase
  // end
  
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

  logic hit_indication;
  assign hit_indication = (tag_0_match && is_valid_way0) || (tag_1_match && is_valid_way1);

  logic tag_array_wen;
  assign tag_array_0_wen = (current_way == 0) ? tag_array_wen : 1'b0;
  assign tag_array_1_wen = (current_way == 1) ? tag_array_wen : 1'b0;

  logic data_array_wen;
  assign data_array_0_wen = (current_way == 0) ? data_array_wen : 1'b0;
  assign data_array_1_wen = (current_way == 1) ? data_array_wen : 1'b0;

  // assign current_way = (hit_indication) ? (tag_0_match) ? 0 : 1 : lru_bit;

  always @(posedge clk or posedge reset) begin
  if (reset) begin
    current_way <= 1'b0; //
  end else if (state_reg == STATE_TAG_CHECK) begin
    // 
    current_way <= (hit_indication) ? (tag_0_match ? 1'b0 : 1'b1) : lru_bit;
  end
  // 
end

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
      if ( proc2cache_reqstream_val ) // When there is a request from the processor, move to TAG_CHECK
        state_next = STATE_TAG_CHECK;
      else
        state_next = STATE_IDLE;        // Stay in idle state
    
    // TAG check state to determine hit or miss
    STATE_TAG_CHECK: begin
      if ( is_init )
          state_next = STATE_INIT_DATA_ACCESS;              // Initialization transaction
      else if ( hit_indication && is_read )
          state_next = STATE_READ_DATA_ACCESS;              // Read hit
      else if ( hit_indication && is_write )
          state_next = STATE_WRITE_DATA_ACCESS;             // Write hit
      else if ( !hit_indication && !is_dirty ) begin
          state_next = STATE_REFILL_REQUEST;                // Miss without dirty
      end else if ( !hit_indication && is_dirty ) begin
          state_next = STATE_EVICT_PREPARE;                 // Miss with dirty, requires eviction
      end
    end

    STATE_INIT_DATA_ACCESS:
      state_next = STATE_WAIT;                  // Initialization transaction, move to wait state
    
    STATE_READ_DATA_ACCESS:
      state_next = STATE_WAIT;                  // Read hit, move to wait state
    
    STATE_WRITE_DATA_ACCESS:
      state_next = STATE_WAIT;                  // Write hit, move to wait state
    
    STATE_EVICT_PREPARE:
      state_next = STATE_EVICT_REQUEST;         // Write miss, move to evict request state
    
    STATE_EVICT_REQUEST:
      if (cache2mem_reqstream_rdy)                // When there is a request from the cache, move to evict wait state
        state_next = STATE_EVICT_WAIT;            // Write miss, move to evict wait state
      else if ( !cache2mem_reqstream_rdy )        // When there is no request from the cache, stay in evict request state
        state_next = STATE_EVICT_REQUEST;
    
    STATE_EVICT_WAIT:
      if(cache2mem_respstream_val)             // When there is a response from the cache, move to refill request state
        state_next = STATE_REFILL_REQUEST;        // Write miss, move to refill request state
      else if ( !cache2mem_respstream_val )    // When there is no response from the cache, stay in evict wait state
        state_next = STATE_EVICT_WAIT;
    
    STATE_REFILL_REQUEST:
      if (cache2mem_reqstream_rdy)                // When there's a request from the cache, move to refill wait state
        state_next = STATE_REFILL_WAIT;           // Read miss, move to refill wait state
      else if ( !cache2mem_reqstream_rdy )        // When there's no request from the cache, stay in refill request state
        state_next = STATE_REFILL_REQUEST;
    
    STATE_REFILL_WAIT:
      if(cache2mem_respstream_val)             // When there's a response from the cache, move to refill update state
        state_next = STATE_REFILL_UPDATE;         // Read miss, move to refill update state
      else if ( !cache2mem_respstream_val )    // When there's no response from the cache, stay in refill wait state
        state_next = STATE_REFILL_WAIT;
    
    STATE_REFILL_UPDATE:
      if(is_read)                               // When there's a read request, move to read data access state
        state_next = STATE_READ_DATA_ACCESS;
      else if (is_write)                        // When there's a write request, move to write data access state
        state_next = STATE_WRITE_DATA_ACCESS;
      else
        state_next = STATE_WAIT;                  // Read miss, move to wait state
    
    STATE_WAIT:
      if(proc2cache_respstream_rdy)             // When there's a response from the cache, move to idle state
        state_next = STATE_IDLE;
      else if ( !proc2cache_respstream_rdy )    // When there's no response from the cache, stay in wait state
        state_next = STATE_WAIT;
    default:
      state_next = STATE_IDLE;

  endcase
end

  //----------------------------------------------------------------------
  // Valid/Dirty bits record
  //----------------------------------------------------------------------

  // Address Mapping

  logic [1:0]   cachereq_addr_byte_offset;
  logic [1:0]   cachereq_addr_word_offset;
  logic [3:0]   cachereq_addr_index;
  logic [23:0]  cachereq_addr_tag;
  logic [1:0]   cachereq_addr_bank;

  generate
    if ( p_num_banks == 1 ) begin
      assign cachereq_addr_byte_offset = cachereq_addr[1:0];
      assign cachereq_addr_word_offset = cachereq_addr[3:2];

      assign cachereq_addr_index       = cachereq_addr[6:4];
      assign cachereq_addr_tag         = cachereq_addr[31:7];
    end
    else if ( p_num_banks == 4 ) begin
      // handle address mapping for four banks
      assign cachereq_addr_byte_offset = cachereq_addr[1:0];
      assign cachereq_addr_word_offset = cachereq_addr[3:2];

      assign cachereq_addr_bank        = cachereq_addr[5:4];
      assign cachereq_addr_index       = cachereq_addr[8:6];
      assign cachereq_addr_tag         = cachereq_addr[31:9];
    end
  endgenerate

  logic valid_bit_in;
  logic valid_bits_write_en;
  logic valid_bits_write_en_way0;
  logic valid_bits_write_en_way1;
  logic is_valid;
  logic is_valid_way0;
  logic is_valid_way1;

  assign is_valid = (current_way == 0) ? is_valid_way0 : is_valid_way1;
  assign valid_bits_write_en_way0 = (current_way == 0) ? valid_bits_write_en : 1'b0;
  assign valid_bits_write_en_way1 = (current_way == 1) ? valid_bits_write_en : 1'b0;


  vc_ResetRegfile_1r1w#(1,8) valid_bits_way0
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_valid_way0),
    .write_en   (valid_bits_write_en_way0),
    .write_addr (cachereq_addr_index),
    .write_data (valid_bit_in)
  );


  vc_ResetRegfile_1r1w#(1,8) valid_bits_way1
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_valid_way1),
    .write_en   (valid_bits_write_en_way1),
    .write_addr (cachereq_addr_index),
    .write_data (valid_bit_in)
  );

  logic dirty_bit_in;
  logic dirty_bits_write_en;
  logic dirty_bits_write_en_way0;
  logic dirty_bits_write_en_way1;
  logic is_dirty;
  logic is_dirty_way0;
  logic is_dirty_way1;
  
  assign is_dirty = (current_way == 0) ? is_dirty_way0 : is_dirty_way1;
  assign dirty_bits_write_en_way0 = (current_way == 0) ? dirty_bits_write_en : 1'b0;
  assign dirty_bits_write_en_way1 = (current_way == 1) ? dirty_bits_write_en : 1'b0;

  vc_ResetRegfile_1r1w#(1,8) dirty_bits_way0
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_dirty_way0),
    .write_en   (dirty_bits_write_en_way0),
    .write_addr (cachereq_addr_index),
    .write_data (dirty_bit_in)
  );

  vc_ResetRegfile_1r1w#(1,8) dirty_bits_way1
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_dirty_way1),
    .write_en   (dirty_bits_write_en_way1),
    .write_addr (cachereq_addr_index),
    .write_data (dirty_bit_in)
  );

  logic lru_bit;
  logic lru_bits_write_en;
  logic lru_bits_in;

  assign lru_bits_in = ~current_way;  // Inverse of current way

  vc_ResetRegfile_1r1w#(1,8) LRU_reg
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (lru_bit),
    .write_en   (lru_bits_write_en),
    .write_addr (cachereq_addr_index),
    .write_data (lru_bits_in)
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
    input logic [1:0] cs_hit,
    input logic [3:0] cs_memreq_type,
    input logic cs_valid_bit_in,
    input logic cs_valid_bits_write_en,
    input logic cs_dirty_bit_in,
    input logic cs_dirty_bits_write_en,
    input logic cs_lru_bits_write_en

  );
  begin
    proc2cache_reqstream_rdy  = cs_cachereq_rdy;          // 1
    proc2cache_respstream_val = cs_cacheresp_val;         // 2     
    cache2mem_reqstream_val   = cs_memreq_val;            // 3
    cache2mem_respstream_rdy  = cs_memresp_rdy;           // 4
    cachereq_reg_en           = cs_cachereq_reg_en;       // 5
    memresp_reg_en            = cs_memresp_reg_en;        // 6
    write_data_mux_sel        = cs_write_data_mux_sel;    // 7
    wben_mux_sel              = cs_wben_mux_sel;          // 8
    tag_array_wen             = cs_tag_array_wen;         // 9
    tag_array_ren             = cs_tag_array_ren;         // 10
    data_array_wen            = cs_data_array_wen;        // 11
    data_array_ren            = cs_data_array_ren;        // 12
    read_data_zero_mux_sel    = cs_read_data_zero_mux_sel;// 13  
    read_data_reg_en          = cs_read_data_reg_en;      // 14
    evict_addr_reg_en         = cs_evict_addr_reg_en;     // 15
    memreq_addr_mux_sel       = cs_memreq_addr_mux_sel;   // 16  
    hit                       = cs_hit;                   // 17
    memreq_type               = cs_memreq_type;           // 18
    valid_bit_in              = cs_valid_bit_in;          // 19
    valid_bits_write_en       = cs_valid_bits_write_en;   // 20
    dirty_bit_in              = cs_dirty_bit_in;          // 21
    dirty_bits_write_en       = cs_dirty_bits_write_en;   // 22
    lru_bits_write_en         = cs_lru_bits_write_en;     // 23
  end
  endtask


  // Set outputs using a control signal "table"
  always @(*) begin
    // Initialize control signals to default values (all zero/off)
    cs( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2'b00, 4'b0000, 0, 0 , 0, 0, 0 );
    case ( state_reg )
      // Control signals for each state
      //                           1     2    3     4    5     6     7     8     9    10    11      12     13     14      15       16     17     18       19     20    21    22    23
      //                          cache cache mem  mem   cache mem   write  wb   tag   tag   data   data   read   read   evict     mem           mem     valid valid   dirty dirty lru
      //                          req   resp  req  resp  req   resp  data   en   array array array  array  zero   data   addr      req    hit    req      bit   write  bit   write write 
      //                          rdy   val   val  rdy   en    en    mux    mux  wen   ren   wen    ren    mux     en     en       mux           type     in    en     in    en    en
      STATE_IDLE:              cs( 1,    0,    0,    0,    1,    0,   0,    0,    0,    0,    0,     0,     0,     0,     0,       0,    2'b00,   4'bx,    0,    0,     0,   0,    0);
      STATE_TAG_CHECK:         cs( 0,    0,    0,    0,    0,    0,   1,    1,    0,    1,    0,     0,     0,     0,     0,       0,    2'bxx ,  4'bx,    0,    0,     0,   0,    0);
      
      STATE_INIT_DATA_ACCESS:  cs( 0,    0,    0,    0,    0,    0,   1,    1,    1,    0,    1,     0,     0,     0,     0,       0,    2'b00,   4'bx,    1,    1,     0,   1,    1);  
      STATE_READ_DATA_ACCESS:  cs( 0,    0,    0,    0,    0,    0,   0,    0,    0,    0,    0,     1,     1,     1,     0,       0,    2'b10,   4'bx,    0,    0,     0,   0,    1); 
      STATE_WRITE_DATA_ACCESS: cs( 0,    0,    0,    0,    0,    0,   1,    1,    1,    0,    1,     0,     0,     1,     0,       0,    2'b10,   4'bx,    1,    1,     1,   1,    1);
      
      STATE_EVICT_PREPARE:     cs( 0,    0,    0,    0,    0,    0,   0,    0,    0,    1,    0,     1,     1,     1,     1,       1,    2'b01,   4'd1,    0,    0,     0,   0,    0);
      STATE_EVICT_REQUEST:     cs( 0,    0,    1,    0,    0,    0,   0,    0,    0,    0,    0,     0,     0,     0,     0,       1,    2'b01,   4'd1,    0,    0,     0,   0,    0);
      STATE_EVICT_WAIT:        cs( 0,    0,    0,    1,    0,    0,   0,    0,    0,    0,    0,     0,     0,     0,     0,       0,    2'b01,   4'd1,    0,    0,     0,   0,    0);

      STATE_REFILL_REQUEST:    cs( 0,    0,    1,    0,    0,    0,   0,    0,    0,    0,    0,     0,     1,     0,     0,       0,    2'b00,   4'd0,    0,    0,     0,   0,    0);
      STATE_REFILL_WAIT:       cs( 0,    0,    0,    1,    0,    1,   0,    0,    0,    0,    0,     0,     0,     0,     0,       0,    2'b00,   4'd0,    0,    0,     0,   0,    0);
      STATE_REFILL_UPDATE:     cs( 0,    0,    0,    0,    0,    0,   0,    0,    1,    0,    1,     0,     0,     0,     0,       0,    2'b10,   4'd0,    1,    1,     0,   1,    0);
      
      STATE_WAIT:              cs( 0,    1,    0,    0,    0,    0,   0,    0,    0,    0,    0,     0,     0,     0,     0,       0,    2'b01,   4'bx,    0,    0,     0,   0,    0);
      default:                 cs( 0,    0,    0,    0,    0,    0,   0,    0,    0,    0,    0,     0,     0,     0,     0,       0,    2'b00,   4'b0,    0,    0,     0,   0,    0);

    endcase
  end



endmodule

`endif
