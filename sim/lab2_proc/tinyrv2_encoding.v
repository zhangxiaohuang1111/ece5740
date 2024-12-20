//========================================================================
// TinyRV2 Instruction Type
//========================================================================
// Instruction types are similar to message types but are strictly used
// for communication within a TinyRV2-based processor. Instruction
// "messages" can be unpacked into the various fields as defined by the
// TinyRV2 ISA, as well as be constructed from specifying each field
// explicitly. The 32-bit instruction has different fields depending on
// the format of the instruction used. The following are the various
// instruction encoding formats used in the TinyRV2 ISA.
//
//  31          25 24   20 19   15 14    12 11          7 6      0
// | funct7       | rs2   | rs1   | funct3 | rd          | opcode |  R-type
// | imm[11:0]            | rs1   | funct3 | rd          | opcode |  I-type, I-imm
// | imm[11:5]    | rs2   | rs1   | funct3 | imm[4:0]    | opcode |  S-type, S-imm
// | imm[12|10:5] | rs2   | rs1   | funct3 | imm[4:1|11] | opcode |  SB-type,B-imm
// | imm[31:12]                            | rd          | opcode |  U-type, U-imm
// | imm[20|10:1|11|19:12]                 | rd          | opcode |  UJ-type,J-imm

`ifndef LAB2_PROC_TINYRV2_ENCODING_V
`define LAB2_PROC_TINYRV2_ENCODING_V

`include "vc/trace.v"

//------------------------------------------------------------------------
// Instruction fields
//------------------------------------------------------------------------

`define TINYRV2_INST_OPCODE  6:0
`define TINYRV2_INST_RD      11:7
`define TINYRV2_INST_RS1     19:15
`define TINYRV2_INST_RS2     24:20
`define TINYRV2_INST_FUNCT3  14:12
`define TINYRV2_INST_FUNCT7  31:25
`define TINYRV2_INST_CSR     31:20

// CUSTOM0 specific

`define TINYRV2_INST_XD      14:14
`define TINYRV2_INST_XS1     13:13
`define TINYRV2_INST_XS2     12:12

//------------------------------------------------------------------------
// Field sizes
//------------------------------------------------------------------------

`define TINYRV2_INST_NBITS          32
`define TINYRV2_INST_OPCODE_NBITS   7
`define TINYRV2_INST_RD_NBITS       5
`define TINYRV2_INST_RS1_NBITS      5
`define TINYRV2_INST_RS2_NBITS      5
`define TINYRV2_INST_FUNCT3_NBITS   3
`define TINYRV2_INST_FUNCT7_NBITS   7
`define TINYRV2_INST_CSR_NBITS      12

//------------------------------------------------------------------------
// Instruction opcodes
//------------------------------------------------------------------------

// Basic instructions

`define TINYRV2_INST_CSRRX 32'b0111111_?????_?????_010_?????_1110011
`define TINYRV2_INST_CSRR  32'b???????_?????_?????_010_?????_1110011
`define TINYRV2_INST_CSRW  32'b???????_?????_?????_001_?????_1110011
`define TINYRV2_INST_NOP   32'b0000000_00000_00000_000_00000_0010011
`define TINYRV2_ZERO       32'b0000000_00000_00000_000_00000_0000000

// Register-register arithmetic, logical, and comparison instructions

`define TINYRV2_INST_ADD   32'b0000000_?????_?????_000_?????_0110011
`define TINYRV2_INST_SUB   32'b0100000_?????_?????_000_?????_0110011
`define TINYRV2_INST_AND   32'b0000000_?????_?????_111_?????_0110011
`define TINYRV2_INST_OR    32'b0000000_?????_?????_110_?????_0110011
`define TINYRV2_INST_XOR   32'b0000000_?????_?????_100_?????_0110011
`define TINYRV2_INST_SLT   32'b0000000_?????_?????_010_?????_0110011
`define TINYRV2_INST_SLTU  32'b0000000_?????_?????_011_?????_0110011
`define TINYRV2_INST_MUL   32'b0000001_?????_?????_000_?????_0110011

// Register-immediate arithmetic, logical, and comparison instructions

`define TINYRV2_INST_ADDI  32'b???????_?????_?????_000_?????_0010011
`define TINYRV2_INST_ANDI  32'b???????_?????_?????_111_?????_0010011
`define TINYRV2_INST_ORI   32'b???????_?????_?????_110_?????_0010011
`define TINYRV2_INST_XORI  32'b???????_?????_?????_100_?????_0010011
`define TINYRV2_INST_SLTI  32'b???????_?????_?????_010_?????_0010011
`define TINYRV2_INST_SLTIU 32'b???????_?????_?????_011_?????_0010011

// Shift instructions

`define TINYRV2_INST_SRA   32'b0100000_?????_?????_101_?????_0110011
`define TINYRV2_INST_SRL   32'b0000000_?????_?????_101_?????_0110011
`define TINYRV2_INST_SLL   32'b0000000_?????_?????_001_?????_0110011
`define TINYRV2_INST_SRAI  32'b0100000_?????_?????_101_?????_0010011
`define TINYRV2_INST_SRLI  32'b0000000_?????_?????_101_?????_0010011
`define TINYRV2_INST_SLLI  32'b0000000_?????_?????_001_?????_0010011

// Other instructions

`define TINYRV2_INST_LUI   32'b???????_?????_?????_???_?????_0110111
`define TINYRV2_INST_AUIPC 32'b???????_?????_?????_???_?????_0010111

// Memory instructions

`define TINYRV2_INST_LW    32'b???????_?????_?????_010_?????_0000011
`define TINYRV2_INST_SW    32'b???????_?????_?????_010_?????_0100011

// Unconditional jump instructions

`define TINYRV2_INST_JAL   32'b???????_?????_?????_???_?????_1101111
`define TINYRV2_INST_JALR  32'b???????_?????_?????_000_?????_1100111

// Conditional branch instructions

`define TINYRV2_INST_BEQ   32'b???????_?????_?????_000_?????_1100011
`define TINYRV2_INST_BNE   32'b???????_?????_?????_001_?????_1100011
`define TINYRV2_INST_BLT   32'b???????_?????_?????_100_?????_1100011
`define TINYRV2_INST_BGE   32'b???????_?????_?????_101_?????_1100011
`define TINYRV2_INST_BLTU  32'b???????_?????_?????_110_?????_1100011
`define TINYRV2_INST_BGEU  32'b???????_?????_?????_111_?????_1100011

// Accelerator custom0

`define TINYRV2_INST_CUST0 32'b???????_?????_?????_???_?????_0001011

//------------------------------------------------------------------------
// Coprocessor registers
//------------------------------------------------------------------------

`define TINYRV2_CPR_PROC2MNGR  12'h7C0
`define TINYRV2_CPR_MNGR2PROC  12'hFC0
`define TINYRV2_CPR_COREID     12'hF14
`define TINYRV2_CPR_NUMCORES   12'hFC1
`define TINYRV2_CPR_STATS_EN   12'h7C1

//------------------------------------------------------------------------
// Helper Tasks
//------------------------------------------------------------------------

module lab2_proc_tinyrv2_encoding_InstTasks();

  //----------------------------------------------------------------------
  // Immediate decoding -- only outputs signals at the width required for
  // line tracing
  //----------------------------------------------------------------------
  function [11:0] imm_i( input [`TINYRV2_INST_NBITS-1:0] inst );
  begin
    // I-type immediate
    imm_i = { inst[31], inst[30:25], inst[24:21], inst[20] };
  end
  endfunction

  function [4:0] imm_shamt( input [`TINYRV2_INST_NBITS-1:0] inst );
  begin
    // I-type immediate, specialized for shift amounts
    imm_shamt = { inst[24:21], inst[20] };
  end
  endfunction

  function [11:0] imm_s( input [`TINYRV2_INST_NBITS-1:0] inst );
  begin
    // S-type immediate
    imm_s = { inst[31], inst[30:25], inst[11:8], inst[7] };
  end
  endfunction

  function [12:0] imm_b( input [`TINYRV2_INST_NBITS-1:0] inst );
  begin
    // B-type immediate
    imm_b = { inst[31], inst[7], inst[30:25], inst[11:8], 1'b0 };
  end
  endfunction

  function [19:0] imm_u_sh12( input [`TINYRV2_INST_NBITS-1:0] inst );
  begin
    // U-type immediate, shifted right by 12
    imm_u_sh12 = { inst[31], inst[30:20], inst[19:12] };
  end
  endfunction

  function [20:0] imm_j( input [`TINYRV2_INST_NBITS-1:0] inst );
  begin
    // J-type immediate
    imm_j = { inst[31], inst[19:12], inst[20], inst[30:25], inst[24:21], 1'b0 };
  end
  endfunction

  //----------------------------------------------------------------------
  // Disasm
  //----------------------------------------------------------------------

  reg [3*8-1:0]                     rs1_str;
  reg [3*8-1:0]                     rs2_str;
  reg [3*8-1:0]                     rd_str;
  reg [9*8-1:0]                     csr_str;
  reg [2*8-1:0]                     funct_str;

  logic [`TINYRV2_INST_RS1_NBITS-1:0] rs1;
  logic [`TINYRV2_INST_RS2_NBITS-1:0] rs2;
  logic [`TINYRV2_INST_RD_NBITS-1:0]  rd;
  logic [`TINYRV2_INST_CSR_NBITS-1:0] csr;
  logic [`TINYRV2_INST_FUNCT7_NBITS-1:0] funct;

  function [25*8-1:0] disasm( input [`TINYRV2_INST_NBITS-1:0] inst );
  begin

    // Unpack the fields

    rs1      = inst[`TINYRV2_INST_RS1];
    rs2      = inst[`TINYRV2_INST_RS2];
    rd       = inst[`TINYRV2_INST_RD];
    csr      = inst[`TINYRV2_INST_CSR];
    // xcel
    funct    = inst[`TINYRV2_INST_FUNCT7];

    // Create fixed-width register specifiers

    if ( rs1 <= 9 )
      $sformat( rs1_str, "x0%0d", rs1 );
    else
      $sformat( rs1_str, "x%d",  rs1 );

    if ( rs2 <= 9 )
      $sformat( rs2_str, "x0%0d", rs2 );
    else
      $sformat( rs2_str, "x%d",  rs2 );

    if ( rd <= 9 )
      $sformat( rd_str, "x0%0d", rd );
    else
      $sformat( rd_str, "x%d",  rd );

    if ( csr == `TINYRV2_CPR_PROC2MNGR )
      $sformat( csr_str, "proc2mngr" );
    else if ( csr == `TINYRV2_CPR_MNGR2PROC )
      $sformat( csr_str, "mngr2proc" );
    else if ( csr == `TINYRV2_CPR_COREID )
      $sformat( csr_str, "coreid   " );
    else if ( csr == `TINYRV2_CPR_NUMCORES )
      $sformat( csr_str, "numcores " );
    else if ( csr == `TINYRV2_CPR_STATS_EN )
      $sformat( csr_str, "stats_en " );
    else
      $sformat( csr_str, "    0x%x", csr );

    $sformat( funct_str, "%x", funct[1:0]);

    // Actual disassembly

    casez ( inst )
      `TINYRV2_INST_CSRR  : $sformat( disasm, "csrr   %s, %s  ",        rd_str,  csr_str );
      `TINYRV2_INST_CSRW  : $sformat( disasm, "csrw   %s, %s  ",        csr_str, rs1_str );
      `TINYRV2_INST_NOP   : $sformat( disasm, "nop                    " );
      `TINYRV2_ZERO       : $sformat( disasm, "                       " );

      `TINYRV2_INST_ADD   : $sformat( disasm, "add    %s, %s, %s   ",   rd_str,  rs1_str, rs2_str );
      `TINYRV2_INST_SUB   : $sformat( disasm, "sub    %s, %s, %s   ",   rd_str,  rs1_str, rs2_str );
      `TINYRV2_INST_AND   : $sformat( disasm, "and    %s, %s, %s   ",   rd_str,  rs1_str, rs2_str );
      `TINYRV2_INST_OR    : $sformat( disasm, "or     %s, %s, %s   ",   rd_str,  rs1_str, rs2_str );
      `TINYRV2_INST_XOR   : $sformat( disasm, "xor    %s, %s, %s   ",   rd_str,  rs1_str, rs2_str );
      `TINYRV2_INST_SLT   : $sformat( disasm, "slt    %s, %s, %s   ",   rd_str,  rs1_str, rs2_str );
      `TINYRV2_INST_SLTU  : $sformat( disasm, "sltu   %s, %s, %s   ",   rd_str,  rs1_str, rs2_str );
      `TINYRV2_INST_MUL   : $sformat( disasm, "mul    %s, %s, %s   ",   rd_str,  rs1_str, rs2_str );

      `TINYRV2_INST_ADDI  : $sformat( disasm, "addi   %s, %s, 0x%x ",   rd_str,  rs1_str, imm_i(inst) );
      `TINYRV2_INST_ANDI  : $sformat( disasm, "andi   %s, %s, 0x%x ",   rd_str,  rs1_str, imm_i(inst) );
      `TINYRV2_INST_ORI   : $sformat( disasm, "ori    %s, %s, 0x%x ",   rd_str,  rs1_str, imm_i(inst) );
      `TINYRV2_INST_XORI  : $sformat( disasm, "xori   %s, %s, 0x%x ",   rd_str,  rs1_str, imm_i(inst) );
      `TINYRV2_INST_SLTI  : $sformat( disasm, "slti   %s, %s, 0x%x ",   rd_str,  rs1_str, imm_i(inst) );
      `TINYRV2_INST_SLTIU : $sformat( disasm, "sltiu  %s, %s, 0x%x ",   rd_str,  rs1_str, imm_i(inst) );

      `TINYRV2_INST_SRA   : $sformat( disasm, "sra    %s, %s, 0x%x  ",  rd_str,  rs1_str, imm_shamt(inst) );
      `TINYRV2_INST_SRL   : $sformat( disasm, "srl    %s, %s, 0x%x  ",  rd_str,  rs1_str, imm_shamt(inst) );
      `TINYRV2_INST_SLL   : $sformat( disasm, "sll    %s, %s, 0x%x  ",  rd_str,  rs1_str, imm_shamt(inst) );
      `TINYRV2_INST_SRAI  : $sformat( disasm, "srai   %s, %s, 0x%x  ",  rd_str,  rs1_str, imm_shamt(inst) );
      `TINYRV2_INST_SRLI  : $sformat( disasm, "srli   %s, %s, 0x%x  ",  rd_str,  rs1_str, imm_shamt(inst) );
      `TINYRV2_INST_SLLI  : $sformat( disasm, "slli   %s, %s, 0x%x  ",  rd_str,  rs1_str, imm_shamt(inst) );

      `TINYRV2_INST_LUI   : $sformat( disasm, "lui    %s, 0x%x    ",    rd_str,  imm_u_sh12(inst));
      `TINYRV2_INST_AUIPC : $sformat( disasm, "auipc  %s, 0x%x    ",    rd_str,  imm_u_sh12(inst));

      `TINYRV2_INST_LW    : $sformat( disasm, "lw     %s, 0x%x(%s) ",   rd_str,  imm_i(inst), rs1_str );
      `TINYRV2_INST_SW    : $sformat( disasm, "sw     %s, 0x%x(%s) ",   rs2_str, imm_s(inst), rs1_str );

      `TINYRV2_INST_JAL   : $sformat( disasm, "jal    %s, 0x%x   ",     rd_str, imm_j(inst) );
      `TINYRV2_INST_JALR  : $sformat( disasm, "jalr   %s, %s, 0x%x ",   rd_str, rs1_str, imm_i(inst) );

      `TINYRV2_INST_BEQ   : $sformat( disasm, "beq    %s, %s, 0x%x",    rs1_str, rs2_str, imm_b(inst) );
      `TINYRV2_INST_BNE   : $sformat( disasm, "bne    %s, %s, 0x%x",    rs1_str, rs2_str, imm_b(inst) );
      `TINYRV2_INST_BLT   : $sformat( disasm, "blt    %s, %s, 0x%x",    rs1_str, rs2_str, imm_b(inst) );
      `TINYRV2_INST_BGE   : $sformat( disasm, "bge    %s, %s, 0x%x",    rs1_str, rs2_str, imm_b(inst) );
      `TINYRV2_INST_BLTU  : $sformat( disasm, "bltu   %s, %s, 0x%x",    rs1_str, rs2_str, imm_b(inst) );
      `TINYRV2_INST_BGEU  : $sformat( disasm, "bgeu   %s, %s, 0x%x",    rs1_str, rs2_str, imm_b(inst) );

      `TINYRV2_INST_CUST0 : $sformat( disasm, "cust0 %s, %s, %s, %s", rd_str, rs1_str, rs2_str, funct_str );
      default             : $sformat( disasm, "illegal inst           " );
    endcase

  end
  endfunction

  //----------------------------------------------------------------------
  // Disasm Tiny
  //----------------------------------------------------------------------

  function [4*8-1:0] disasm_tiny( input [`TINYRV2_INST_NBITS-1:0] inst );
  begin

    casez ( inst )
      `TINYRV2_INST_CSRR  : disasm_tiny = "csrr";
      `TINYRV2_INST_CSRW  : disasm_tiny = "csrw";
      `TINYRV2_INST_NOP   : disasm_tiny = "nop ";

      `TINYRV2_INST_ADD   : disasm_tiny = "add ";
      `TINYRV2_INST_SUB   : disasm_tiny = "sub ";
      `TINYRV2_INST_AND   : disasm_tiny = "and ";
      `TINYRV2_INST_OR    : disasm_tiny = "or  ";
      `TINYRV2_INST_XOR   : disasm_tiny = "xor ";
      `TINYRV2_INST_SLT   : disasm_tiny = "slt ";
      `TINYRV2_INST_SLTU  : disasm_tiny = "sltu";
      `TINYRV2_INST_MUL   : disasm_tiny = "mul ";

      `TINYRV2_INST_ADDI  : disasm_tiny = "addi";
      `TINYRV2_INST_ANDI  : disasm_tiny = "andi";
      `TINYRV2_INST_ORI   : disasm_tiny = "ori ";
      `TINYRV2_INST_XORI  : disasm_tiny = "xori";
      `TINYRV2_INST_SLTI  : disasm_tiny = "slti";
      `TINYRV2_INST_SLTIU : disasm_tiny = "sltI";

      `TINYRV2_INST_SRA   : disasm_tiny = "sra ";
      `TINYRV2_INST_SRL   : disasm_tiny = "srl ";
      `TINYRV2_INST_SLL   : disasm_tiny = "sll ";
      `TINYRV2_INST_SRAI  : disasm_tiny = "srai";
      `TINYRV2_INST_SRLI  : disasm_tiny = "srli";
      `TINYRV2_INST_SLLI  : disasm_tiny = "slli";

      `TINYRV2_INST_LUI   : disasm_tiny = "lui ";
      `TINYRV2_INST_AUIPC : disasm_tiny = "auiP";

      `TINYRV2_INST_LW    : disasm_tiny = "lw  ";
      `TINYRV2_INST_SW    : disasm_tiny = "sw  ";

      `TINYRV2_INST_JAL   : disasm_tiny = "jal ";
      `TINYRV2_INST_JALR  : disasm_tiny = "jalr";

      `TINYRV2_INST_BEQ   : disasm_tiny = "beq ";
      `TINYRV2_INST_BNE   : disasm_tiny = "bne ";
      `TINYRV2_INST_BLT   : disasm_tiny = "blt ";
      `TINYRV2_INST_BGE   : disasm_tiny = "bge ";
      `TINYRV2_INST_BLTU  : disasm_tiny = "bltu";
      `TINYRV2_INST_BGEU  : disasm_tiny = "bgeu";

      `TINYRV2_INST_CUST0 : disasm_tiny = "cus0";

      default            : disasm_tiny = "????";
    endcase

  end
  endfunction

endmodule


//------------------------------------------------------------------------
// Unpack instruction 
// This is the actual decoding unit
//------------------------------------------------------------------------

module lab2_proc_tinyrv2_encoding_InstUnpack
(
  // Packed message

  input  [`TINYRV2_INST_NBITS-1:0]        inst,

  // Packed fields

  output [`TINYRV2_INST_OPCODE_NBITS-1:0] opcode,
  output [`TINYRV2_INST_RD_NBITS-1:0]     rd,
  output [`TINYRV2_INST_RS1_NBITS-1:0]    rs1,
  output [`TINYRV2_INST_RS2_NBITS-1:0]    rs2,
  output [`TINYRV2_INST_FUNCT3_NBITS-1:0] funct3,
  output [`TINYRV2_INST_FUNCT7_NBITS-1:0] funct7,
  output [`TINYRV2_INST_CSR_NBITS-1:0]    csr
);

  assign opcode   = inst[`TINYRV2_INST_OPCODE];
  assign rd       = inst[`TINYRV2_INST_RD];
  assign rs1      = inst[`TINYRV2_INST_RS1];
  assign rs2      = inst[`TINYRV2_INST_RS2];
  assign funct3   = inst[`TINYRV2_INST_FUNCT3];
  assign csr      = inst[`TINYRV2_INST_CSR];

endmodule

//------------------------------------------------------------------------
// Convert message to string
//------------------------------------------------------------------------

`ifndef SYNTHESIS

module lab2_proc_tinyrv2_encoding_InstTrace
(
  input                           clk,
  input                           reset,
  input [`TINYRV2_INST_NBITS-1:0] inst
);

  lab2_proc_tinyrv2_encoding_InstTasks tinyrv2();

  `VC_TRACE_BEGIN
  begin
    vc_trace.append_str( trace_str, tinyrv2.disasm( inst ) );
    vc_trace.append_str( trace_str, " | " );
    vc_trace.append_str( trace_str, tinyrv2.disasm_tiny( inst ) );
  end
  `VC_TRACE_END

endmodule

`endif /* SYNTHESIS */

`endif /* LAB2_PROC_TINYRV2_ENCODING_V */

