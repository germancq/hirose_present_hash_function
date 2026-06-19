/**
 * @ Author: German Cano Quiveu, germancq@dte.us.es
 * @ Create Time: 2020-03-07 17:39:46
 * @ Modified by: Your name
 * @ Modified time: 2020-04-04 23:22:04
 * @ Description:
 */


module hirose_present(
    input clk,
    input rst,
    input [63:0] c,
    input [15:0] plaintext,
    input [63:0] prev_left_value,
    input [63:0] prev_right_value,
    output end_hash,
    output [127:0] hash_o
);

    logic rst_present;
    
    logic [63:0] input_left;
    logic [63:0] input_right;
    logic [63:0] output_left;
    logic [63:0] output_right;

    assign input_left = prev_left_value;
    assign input_right = prev_left_value ^ c;

    logic [79:0] key_i;
    assign key_i = {prev_right_value,plaintext};
    
    assign hash_o = rst ? 128'h0 : {output_left ^ input_left,
                                    output_right ^ input_right};

    logic end_left;
    logic end_rigth;
    logic end_key_generation_left;
    logic end_key_generation_right;
    assign end_hash = end_key_generation_left & end_key_generation_right & end_left & end_rigth;

    present present_left(
        .clk(clk),
        .rst(rst),
        .end_key_generation(end_key_generation_left),
        .key(key_i),
        .block_i(input_left),
        .block_o(output_left),
        .enc_dec(1'b0),
        .end_signal(end_left)
    );

    present present_right(
        .clk(clk),
        .rst(rst),
        .end_key_generation(end_key_generation_right),
        .key(key_i),
        .block_i(input_right),
        .block_o(output_right),
        .enc_dec(1'b0),
        .end_signal(end_rigth)
    );

    


endmodule : hirose_present