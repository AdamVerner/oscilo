/*
 *
 *  Simple trigger mechanism for both edge detection.
 *  Bounds provide some noise cancelation on trigger.
 *  They can be set to same values to disable this mechanism.
 *  rising and falling edge detection can be enabled simoutanously
 *  once the trigger is set it needs to be reseted to be used again
 *
 *  trig_rst is for reseting from sampler
 *  rst is for global resets
 *
 */

module trigger(
    input clk,

    input rst,

    input trig_rst,

    input [WIDTH-1:0] data, upper_bound, lower_bound,
    input en_rise, en_fall,

    output trigger

);
    parameter WIDTH = 8;

    logic is_upper=0, is_lower=0, trig=0;

    assign trigger = trig;  // stage the output

    always @(posedge clk) begin
        if (~rst || trig_rst) begin
            is_upper = 0;
            is_lower = 0;
            trig = 0;
        end else if (en_fall) begin
            if (data > upper_bound) begin
                is_upper = 1;
                is_lower = 0;
            end
            if (is_upper && (data < lower_bound))
                trig = 1;
        end else if (en_rise) begin
            if (data < upper_bound) begin
                is_lower = 1;
                is_upper = 0;
            end
            if (is_lower && (data > upper_bound))
                trig = 1;
        end
    end

endmodule