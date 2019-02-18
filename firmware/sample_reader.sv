/*
*/

module sampler(

    input        clk_50mhz,
                 reset,

    input        activate, // drive to 1 to activate the module
    output       done = 0,    // signals that the module has done what it needed to do

    input        tx_active,
    output [7:0] tx_data,
    output       tx_start,

    input [7:0]  mem_data,
    output [7:0] mem_addr = 0,
    output       mem_oe = 0
);

    reg [22:0] sleep_counter;  // max = 8388607
    wire [3:0]              reader_state;

    parameter ST_IDLE = 0;
    parameter ST_FETCH = 1;
    parameter ST_TX = 2;
    parameter ST_DONE = 3;


    always @(posedge clk_50mhz)begin

    end

    always @(posedge std_clk)
        begin
            case (sampler_state)
                ST_IDLE:
                begin
                    if (activate)
                    begin
                        sampler_state = ST_FETCH;
                        mem_addr = 0;
                        mem_oe = 1;
                    end
                end
                ST_FETCH:
                begin
                    tx_data = mem_data;
                    mem_addr += 1;

                    if(mem_addr >= 255)
                        sampler_state = ST_DONE;
                    else
                    begin
                        tx_start = 1;
                        stampler_state = ST_TX;
                    end
                end
                ST_TX:
                begin
                    if(~tx_active)
                    begin
                        tx_start = 0;
                        sampler_state = ST_WAIT;
                    end
                end
                ST_WAIT:
                begin
                    sleep_counter = sleep_counter + 1;
                    if(sleep_counter >= 5000000) // wait 0.1 sec
                        state = ST_FETCH;
                end
                ST_DONE:
                begin
                    sampler_state = ST_IDLE;
                    tx_start = 0;
                    mem_oe = 0;

                end

                default:
                    sampler_state = ST_IDLE;
            endcase
        end

endmodule
