/*
*   statemodule
*   the hearth of the whole osciloscope
*   TODO shift the memory, so the first sample is on the first place in
*   memmory
*   TODO more advanced trigger logic (external module)
*/

module sampler(

    input        clk_50mhz,
                 reset,

    input        activate, // drive to 1 to activate the module
    output       done = 0,    // signals that the module has done what it needed to do

    output       adc_clk,
    input  [7:0] adc_data,

    output       mem_clk,
    output [7:0] mem_data,
    output [7:0] mem_addr,
    output       mem_we
);

    parameter SAMPLE_DEPTH = 8; // 256 samples

    wire [SAMPLE_DEPTH-1:0] samples_trigger_offset;
    wire [SAMPLE_DEPTH-1:0] remaining_samples;
    wire                    activate_adc_clk;
    wire                    activate_mem_clk;
    wire                    trig;

    wire [3:0]              sampler_state;

    parameter ST_IDLE = 0;
    parameter ST_SETUP = 1;
    parameter ST_PRE_TRIG = 2;
    parameter ST_POST_TRIG = 3;
    parameter ST_SHIFT = 4;
    parameter ST_CLEAR = 5;


        // activate output adc only when activated
    assign adc_clk = clk_50mhz && activate_adc_clk;
    assign mem_clk = clk_50mhz && activate_mem_clk;


        // TRIGGER LOGIC BEGIN
    reg                     thr1, thr2;
    always @(posedge adc_clk)
        begin
            thr1 <= (adc_data >= 8'h80);
            thr2 <= thr1;
        end
    assign trig = thr1 & ~thr2; /* assert true for one clock*/
        // TRIGGER LOGIC END


        /* TODO add clk_divided*/

    always @(posedge clk_50mhz)
        begin
            case (sampler_state)

                ST_IDLE:
                    if (activate)
                        sampler_state = ST_SETUP;

                ST_SETUP: begin
                    done = 0;
                    activate_adc_clk = 1;
                    activate_mem_clk = 1;
                    mem_we = 1;  // enable writing into memory
                    mem_addr = 0;  // start from zero
                    sampler_state = ST_PRE_TRIG;
                    remaining_samples = (1 << (SAMPLE_DEPTH-1))-1; // half of samples
                end

                /* store samples in memmory and add 1 to address and let it
                * overflow indefinitley (redneck circular-buffer) */
                ST_PRE_TRIG: begin
                    mem_addr = mem_addr+1;
                    mem_data = adc_data;
                    if (trig)
                        begin
                            sampler_state = ST_POST_TRIG;
                            samples_trigger_offset = mem_addr;
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
                    sampler_state = ST_CLEAR;
                /* TODO shift samples */
                ST_CLEAR:
                    begin
                        activate_adc_clk = 0;
                        activate_mem_clk = 0;
                        mem_we = 0;  // enable writing into memory
                        done = 1;
                        sampler_state = ST_IDLE;
                    end

                default:
                    sampler_state = ST_IDLE;
            endcase
        end


endmodule
