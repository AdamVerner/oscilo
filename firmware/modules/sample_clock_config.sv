/*
 *  1. byte = upper byte
 *  2. byte = lower byte
 *  default is to divide 0 times (full speed)
 */

module sample_clock_config(
    /* std module signals */
    input         clk,
                  rst,
                  activate,
    output        done,

    input  [7:0]  rx_data,
    input         rx_ready,

    output [15:0] clk_div = 0
);


    reg [7:0] msb;

    reg [2:0] conf_state = 0;
    parameter ST_IDLE = 0;
    parameter ST_RECV_FIRST = 1;
    parameter ST_RECV_SECOND = 2;
    parameter ST_CLEAR = 3;

    always @(posedge clk) begin

        if (~rst) begin
            conf_state = ST_IDLE;
            clk_div = 0;
        end

        case (conf_state)
            ST_IDLE: begin
                done = 0;
                if (activate)
                    conf_state = ST_RECV_FIRST;
            end
            ST_RECV_FIRST: begin
                if (rx_ready) begin  // rx_ready should be on for only one clk cycle
                    msb = rx_data;
                    conf_state = ST_RECV_SECOND;
                end
            end
            ST_RECV_SECOND: begin
                if (rx_ready) begin  // rx_ready should be on for only one clk cycle
                    clk_div = {msb, rx_data};
                    conf_state = ST_CLEAR;
                end
            end
            ST_CLEAR: begin
                done = 1;
                if (~activate)
                    conf_state = ST_IDLE;
            end
            default: conf_state = ST_IDLE;
        endcase
    end

endmodule
