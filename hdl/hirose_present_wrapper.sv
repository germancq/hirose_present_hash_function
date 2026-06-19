/**
 * @ Author: German Cano Quiveu, germancq
 * @ Create Time: 2019-10-14 15:28:48
 * @ Modified by: Your name
 * @ Modified time: 2020-04-13 21:38:21
 * @ Description:
 */


module hirose_present_wrapper #(parameter DATA_WIDTH = 64)
(
    input clk,
    input rst,
    input [DATA_WIDTH-1:0] plaintext,
    input [63:0] c,
    output [127:0] hash_output,
    output logic end_signal
);

    

   logic rst_hash;
    logic [15:0] hash_plaintext;
    logic end_hash;
    logic [127:0] hash_o;


    logic h_left_w;
    logic [63:0] h_left_o;
    

    logic h_right_w;
    logic [63:0] h_right_o;

    assign hash_output = {h_left_o,h_right_o};


    hirose_present hash_impl(
        .clk(clk),
        .rst(rst_hash),
        .c(c),
        .plaintext(hash_plaintext),
        .prev_left_value(h_left_o),
        .prev_right_value(h_right_o),
        .end_hash(end_hash),
        .hash_o(hash_o)
    );

    logic [$clog2(DATA_WIDTH)-1:0] counter_output;
    logic counter_up;

    counter #(.DATA_WIDTH($clog2(DATA_WIDTH))) counter_impl(
        .clk(clk),
        .rst(rst),
        .up(counter_up),
        .down(1'b0),
        .din({$clog2(DATA_WIDTH){1'b0}}),
        .dout(counter_output)
    );


    
    

    register #(.DATA_WIDTH(64)) H_left(
        .clk(clk),
        .cl(rst),
        .w(h_left_w),
        .din(hash_o[127:64]),
        .dout(h_left_o)
    );

    register #(.DATA_WIDTH(64)) H_right(
        .clk(clk),
        .cl(rst),
        .w(h_right_w),
        .din(hash_o[63:0]),
        .dout(h_right_o)
    );


    typedef enum logic [2:0] {IDLE,RST_HASH,WAIT_FOR_ENC,WRITE_PREV_VALUES,END} state_t;
    state_t current_state, next_state;

    assign hash_plaintext = 16'(plaintext >> (counter_output<<4));

    

    always_comb begin

        next_state = current_state;

        counter_up = 0;
        h_left_w = 0;
        h_right_w = 0;
        rst_hash = 0;

        end_signal = 0;

        

        case(current_state)
            IDLE : 
                begin
                    rst_hash = 1;
                    h_left_w = 1'b1;
                    h_right_w = 1'b1;
                    
                    next_state = WAIT_FOR_ENC;
                end
            RST_HASH :
                begin
                    rst_hash = 1'b1;
                    next_state = WAIT_FOR_ENC;
                end    
            WAIT_FOR_ENC :
                begin
                    if(end_hash) begin
                        next_state = WRITE_PREV_VALUES;
                    end
                end    
            WRITE_PREV_VALUES :
                begin
                    h_left_w = 1'b1;
                    h_right_w = 1'b1;
                    counter_up = 1'b1;
                    if(counter_output == $clog2(DATA_WIDTH)'(DATA_WIDTH>>4)-1 ) begin
                        next_state = END;
                    end
                    else begin
                        
                        next_state = RST_HASH;
                    end
                end    
            END :
                begin
                    end_signal = 1'b1;
                end    
            default:;
        endcase
    end


    always_ff @(posedge clk) begin
        if (rst) begin
            current_state <= IDLE;
        end
        else begin
            current_state <= next_state;
        end
    end


endmodule : hirose_present_wrapper