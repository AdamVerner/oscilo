/*
*/

module sample_offset(

    input        clk_50mhz,
                 reset,

    input        activate, // drive to 1 to activate the module
    output       done = 0,    // signals that the module has done what it needed to do

    input        tx_active,
    output [7:0] tx_data,
    output       tx_start = 0,

    input  [SAMPLE_DEPTH-1:0] offset

);

    parameter offset = 32'h12345678;

    parameter SAMPLE_DEPTH = 8;

    reg [22:0] sleep_counter;  // max = 8388607
    reg [4:0] getter_state;

    parameter ST_IDLE = 0;
    parameter ST_SEND1 = 1;
    parameter ST_WAIT1 = 2;
    parameter ST_SEND2 = 3;
    parameter ST_WAIT2 = 4;
    parameter ST_SEND3 = 5;
    parameter ST_WAIT3 = 6;
    parameter ST_SEND4 = 7;
    parameter ST_WAIT4 = 8;
    parameter ST_CLEAR = 9;

    always @(posedge clk_50mhz)
        begin
            case (getter_state)
                ST_IDLE: begin
                    done = 0;
                    tx_start = 0;
                    if (activate) begin
                        tx_data = ( offset & 32'hff000000 ) >> 24;
                        getter_state = ST_SEND1;
                        tx_start = 1;
                    end
                end
                ST_SEND1: begin
                    getter_state = ST_WAIT1;
                end
                ST_WAIT1: begin
                    if (~tx_active) begin
                        tx_start = 0;
                        tx_data  = ( offset & 32'h00ff0000 ) >> 16;
                        getter_state = ST_SEND2;
                        tx_start = 1;
                    end
                end
                ST_SEND2: begin
                    getter_state = ST_WAIT2;
                end
                ST_WAIT2: begin
                    if (~tx_active)begin
                        tx_start = 0;
                        tx_data  = ( offset & 32'h0000ff00 ) >> 8;
                        getter_state = ST_SEND3;
                        tx_start = 1;
                    end
                end
                ST_SEND3: begin
                    getter_state = ST_WAIT3;
                end
                ST_WAIT3: begin
                    if (~tx_active) begin
                        tx_start = 0;
                        tx_data  = offset & 32'h000000ff;
                        tx_start = 1;
                        getter_state = ST_SEND4;
                    end
                end

                ST_SEND4: getter_state = ST_WAIT4;
                ST_WAIT4: if (~tx_active) getter_state = ST_CLEAR;

                ST_CLEAR: begin
                    done = 1;
                    if (~activate)
                        getter_state = ST_IDLE;
                end
                default:
                    getter_state = ST_IDLE;
            endcase
        end
endmodule
