/*
 *  1. byte = mode ( 1 = rise, 2 = fall, 3 = both, 4 = none, else rise )
 *  2. byte = lower_bound
 *  3. byte = upper_bound
 *
 *  default is to trigger at 50% and at rising edge
 *
 */

module trig_config(
    /* std module signals */
    input clk, rst, activate,
    output done,

    input [7:0]  rx_data,
    input        rx_ready,

    output       en_rise = 1,
    output       en_fall = 0,
    output [7:0] upper_bound = 127,
    output [7:0] lower_bound = 127
);

    reg [3:0] conf_state = 0;
    parameter ST_IDLE = 0;
    parameter ST_RECV_MODE = 1;
    parameter ST_RECV_L_BND = 2;
    parameter ST_RECV_U_BND = 3;
    parameter ST_CLEAR = 4;

    always @(posedge clk) begin

        if(~rst) begin
            conf_state = ST_IDLE;
            en_rise = 1;
            en_fall = 0;
            upper_bound = 127;
            lower_bound = 127;
        end

        case(conf_state)
            ST_IDLE: begin
                done = 0;
                if (activate)
                    conf_state = ST_RECV_MODE;
            end
            ST_RECV_MODE: begin
                if (rx_ready) begin  // rx_ready should be on for only one clk cycle
                    conf_state = ST_RECV_L_BND;
                    if (rx_data == 1) begin
                        en_rise = 1;
                        en_fall = 0;
                    end
                    else if (rx_data == 2) begin
                        en_rise = 0;
                        en_fall = 1;
                    end
                    else if (rx_data == 3) begin
                        en_rise = 1;
                        en_fall = 1;
                    end else if (rx_data == 4) begin
                        en_rise = 0;
                        en_fall = 0;
                    end
                    else begin
                        en_rise = 1;
                        en_fall = 0;
                    end
                end
            end
            ST_RECV_L_BND: begin
                if (rx_ready) begin
                    conf_state = ST_RECV_U_BND;
                    lower_bound = rx_data;
                end
            end
            ST_RECV_U_BND: begin
                if (rx_ready) begin
                    conf_state = ST_CLEAR;
                    upper_bound = rx_data;
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
