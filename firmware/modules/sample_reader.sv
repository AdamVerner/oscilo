/*
 * send two bytes for each memmory adress, starting from 0
 *  MSB0 LSB0 MSB1 LSB1........
 */

module sample_reader(

    input        clk_50mhz,
                 reset,

    input        activate, // drive to 1 to activate the module
    output       done = 0,    // signals that the module has done what it needed to do

    input             tx_active,
    output [7:0]      tx_data,
    output            tx_start,

    input [WIDTH-1:0] mem_data,
    output            mem_oe = 0,	
    output [SAMPLE_DEPTH-1:0] mem_addr = 0
);

    parameter SAMPLE_DEPTH = 0;
    parameter WIDTH = 12;

    wire [2:0] reader_state;

    parameter ST_IDLE = 0;
    parameter ST_FETCH = 1;
    parameter ST_TX = 2;
    parameter ST_SLP = 6;
    parameter ST_SLP2 = 7;

    parameter ST_FETCH_SEC = 3;
    parameter ST_TX_SEC = 4;

    parameter ST_DONE = 5;

    always @(posedge clk_50mhz)
        begin
            case (reader_state)
                ST_IDLE:
                begin
                    done = 0;
                    if (activate)
                    begin
                        reader_state = ST_FETCH;
                        mem_addr = 0;
                        mem_oe = 1;
                    end
                end
                ST_FETCH:
                begin
                    tx_data = (mem_data & 12'hF00) >> 8;
                    tx_start = 1;
                    reader_state = ST_TX;
                end
                ST_TX:
                begin
                    if(~tx_active)
                    begin
                        tx_start = 0;
                        reader_state = ST_SLP;
                    end
                end
                ST_SLP: reader_state = ST_SLP2;
                ST_SLP2: reader_state = ST_FETCH_SEC;
                ST_FETCH_SEC:
                begin
                    tx_data = mem_data & 12'h0FF;
                    tx_start = 1;
                    reader_state = ST_TX_SEC;
                end
                ST_TX_SEC:
                begin
                    if(~tx_active)
                    begin
                        tx_start = 0;
                        if(mem_addr == (1 << SAMPLE_DEPTH)-1)
                            reader_state = ST_DONE;
                        else reader_state = ST_FETCH;

                        mem_addr += 1;
					  end
                end
                ST_DONE:
                begin
                    done = 1;
                    tx_start = 0;
                    mem_oe = 0;
                    if (~activate & ~tx_active)
                        reader_state = ST_IDLE;

                end
                default:
                    reader_state = ST_IDLE;
            endcase
        end

endmodule
