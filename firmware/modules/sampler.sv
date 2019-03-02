/*
 * module, that provides sampling logic to the osciloscope
 * can be force-triggered by seinding 0x55 during pre-trigger state
 * after receiving all memmory the device transimts 0x55 signal
 *
 */

module sampler(
    input                     clk_50mhz,
                              reset,

    input                     activate, // drive to 1 to activate the module
    output                    done = 0,    // signals that the module has done what it needed to do

    output                    adc_clk,
    input  [7:0]              adc_data,

    output                    mem_clk,
    output [7:0]              mem_data,
    output                    mem_we,
    output [SAMPLE_DEPTH-1:0] mem_addr,
    output [SAMPLE_DEPTH-1:0] offset,

    input                     trig,
    output                    trig_reset = 1,
    input                     force_trig,

    input                     rx_ready,
    input  [7:0]              rx_data,

    input                     tx_active,
    output                    tx_start = 0,
    output [7:0]              tx_data = 8'h55,

    input  [15:0]             clk_div
    );

    parameter SAMPLE_DEPTH = 8; // 256 samples


    wire std_clk;
    divider std_clock_divider(
        .clk    (clk_50mhz),
        .count  (clk_div),
        .out_clk(std_clk)
    );

    wire [SAMPLE_DEPTH-1:0] remaining_samples;
    wire                    activate_adc_clk;
    wire                    activate_mem_clk;

    wire [3:0]              sampler_state;

    reg received;
    reg watch_trig = 0;
    reg [7:0] rec_data;

    always @(posedge rx_ready, negedge watch_trig) begin
        if (~watch_trig)
            received <= 0;
        else
        if (rx_ready) begin
            received <= 1;
            rec_data <= rx_data;
        end

    end

    parameter ST_IDLE = 0;
    parameter ST_SETUP = 1;
    parameter ST_ACQUIRE = 2;
    parameter ST_PRE_TRIG = 3;
    parameter ST_POST_TRIG = 4;
    parameter ST_SHIFT = 5;
    parameter ST_SIGNAL = 6;
    parameter ST_CLEAR = 7;


        // activate output adc only when activated
    assign adc_clk = std_clk && activate_adc_clk;
    assign mem_clk = std_clk && activate_mem_clk;

        /* TODO add clk_divided*/

    always @(posedge std_clk)
        begin
            case (sampler_state)

                ST_IDLE:
                begin
                    done = 0;
                    if (activate)
                        sampler_state = ST_SETUP;
                 end

                ST_SETUP: begin
                    activate_adc_clk = 1;
                    activate_mem_clk = 1;
                    mem_we = 1;  // enable writing into memory
                    mem_addr = 0;  // start from zero
                    sampler_state = ST_ACQUIRE;
                    remaining_samples = (1 << (SAMPLE_DEPTH-1))-1; // half of samples
                end

                ST_ACQUIRE: begin  /* get at least 128 samples, BEFORE the trigger */
                    mem_addr = mem_addr + 1;
                    mem_data = adc_data;
                    trig_reset = 1;
                    if (mem_addr >= (1 << (SAMPLE_DEPTH - 1)) - 1)
                        sampler_state = ST_PRE_TRIG;
                end

                /* store samples in memmory and add 1 to address and let it
                * overflow indefinitley (redneck circular-buffer) */
                ST_PRE_TRIG: begin
                    trig_reset = 0;
                    mem_addr = mem_addr+1;
                    mem_data = adc_data;
                    watch_trig = 1;
                    if (trig || force_trig || (received && (rec_data == 8'h55)))
                        begin
                            sampler_state = ST_POST_TRIG;
                            offset = mem_addr;
                        end
                end
                ST_POST_TRIG:
                    begin
                        mem_addr = mem_addr+1;
                        mem_data = adc_data;

                        remaining_samples = remaining_samples-1;
                        if (remaining_samples == 0)
                            sampler_state = ST_SHIFT;
                    end
                ST_SHIFT:
                    sampler_state = ST_SIGNAL;
                /* TODO shift samples */
                ST_SIGNAL: begin
                    tx_data = 8'h55;
                    if (~tx_active) begin
                        tx_start = 1;
                        sampler_state = ST_CLEAR;
                    end
                end
                ST_CLEAR:
                    begin
                        activate_adc_clk = 0;
                        activate_mem_clk = 0;
                        mem_we = 0;  // enable writing into memory
                        done = 1;
                        tx_start = 0;
                        watch_trig = 0;

                        if (~activate && ~tx_active)
                            sampler_state = ST_IDLE;
                    end

                default:
                    sampler_state = ST_IDLE;
            endcase
        end


endmodule
