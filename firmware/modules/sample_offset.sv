/*
*/

module sample_offset(

    input        clk_50mhz,
                 reset,

    input        activate, // drive to 1 to activate the module
    output       done = 0,    // signals that the module has done what it needed to do

    input        tx_active,
    output [7:0] tx_data,
    output       tx_start,

    input  [7:0] offset
);

    reg [3:0] getter_state;
    parameter ST_IDLE = 0;
    parameter ST_SEND = 1;
    parameter ST_CLEAR = 2;

    always @(posedge clk_50mhz)
        begin
            case (getter_state)
                ST_IDLE: begin
                    done = 0;
                    if (activate) begin
                        getter_state = ST_SEND;
                        tx_data = offset;
                        tx_start = 1;
                    end
                end
                ST_SEND: begin
                    if (~tx_active)
                        getter_state = ST_CLEAR;
                end
                ST_CLEAR:
                begin
                    done = 1;
                    tx_start = 0;
                    if (~activate)
                        getter_state = ST_IDLE;
                end
                default:
                    getter_state = ST_IDLE;
            endcase
        end

endmodule
