/*
 *  module for choosing adc for sampler
 *  similar to media access module
 *  currently supporst 3 different adcs, but another one can be simply copied in
 *  always chooses adc1 as default adc in case of invalid message
 *  can support upto 255 ADCs
 *
 *  after activating module recieve one byte of information about which adc to select.
 *
 */

module adc_selector(
    /* std module signals */
    input clk, rst, activate,
    output done,

    input [7:0] rx_data,
    input       rx_ready,

    input [WIDTH-1:0]  adc1_data,
    output             adc1_clk,
    input [WIDTH-1:0]  adc2_data,
    output             adc2_clk,
    input [WIDTH-1:0]  adc3_data,
    output             adc3_clk,

    output [WIDTH-1:0] adc_data,
    input              adc_clk
);

    parameter WIDTH = 8;

    reg adc1_select = 1;
    reg adc2_select = 0;
    reg adc3_select = 0;

    reg [3:0] selector_state;
    parameter ST_IDLE = 0;
    parameter ST_RECV = 1;
    parameter ST_CLEAR = 2;


    assign adc1_clk = adc_clk & adc1_select;
    assign adc2_clk = adc_clk & adc2_select;
    assign adc3_clk = adc_clk & adc3_select;

    assign adc_data = (adc1_data & {WIDTH{adc1_select}}) |
                      (adc2_data & {WIDTH{adc2_select}}) |
                      (adc3_data & {WIDTH{adc3_select}});

    always @(posedge clk) begin

        if(~rst) begin
            selector_state = ST_IDLE;
            adc1_select = 1;
            adc2_select = 0;
            adc3_select = 0;
        end

        case(selector_state)
            ST_IDLE: begin
                done = 0;
                if (activate)
                    selector_state = ST_RECV;
            end
            ST_RECV: begin
                if (rx_ready) begin
                    if(rx_data == 8'h02) begin
                        adc1_select = 0;
                        adc2_select = 1;
                        adc3_select = 0;
                    end else if(rx_data == 8'h03) begin
                        adc1_select = 0;
                        adc2_select = 0;
                        adc3_select = 1;
                    end else begin
                        adc1_select = 1;
                        adc2_select = 0;
                        adc3_select = 0;
                    end
                    selector_state = ST_CLEAR;
                end
            end
            ST_CLEAR: begin
                done = 1;
                if (~activate)
                    selector_state = ST_IDLE;
            end
            default: selector_state = ST_IDLE;
        endcase
    end

endmodule