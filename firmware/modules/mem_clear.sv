module mem_clear(

    input        clk_50mhz,
                 reset,

    input        activate, // drive to 1 to activate the module
    output       done = 0,    // signals that the module has done what it needed to do

    input [7:0]  rx_data,
    input        rx_ready,

    output       mem_clk,
    output [WIDTH-1:0] mem_data,
    output [SAMPLE_DEPTH-1:0] mem_addr,
    output       mem_we
);

    parameter SAMPLE_DEPTH = 8;
    parameter WIDTH = 8;

    reg [3:0] sampler_state;
    parameter ST_IDLE = 0;
    parameter ST_RECV = 1;
    parameter ST_WRITE = 2;
    parameter ST_CLEAR = 3;

    reg [WIDTH-1:0] write_word;

    reg       enable_mem_clk;
    assign mem_clk = clk_50mhz && enable_mem_clk;

    always @(posedge clk_50mhz)
        begin
            case (sampler_state)

                ST_IDLE: begin
                    done = 0;
                    enable_mem_clk = 0;

                    if (activate)
                        sampler_state = ST_RECV;
                 end

                ST_RECV: begin
                    if (rx_ready) begin
                        write_word = rx_data;
                        sampler_state = ST_WRITE;
                        mem_addr = 0;
                    end
                end

                ST_WRITE: begin
                    enable_mem_clk = 1;
                    mem_we = 1;
                    mem_addr += 1;
                    mem_data = write_word;
                    if (mem_addr == (1 << SAMPLE_DEPTH)-1 ) begin
                      sampler_state = ST_CLEAR;
                    end
                end

                ST_CLEAR: begin
                    enable_mem_clk = 0;
                    mem_we = 0;
                    done = 1;

                    if (~activate)
                        sampler_state = ST_IDLE;
                end
            endcase
        end
endmodule
