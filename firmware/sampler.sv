/*
*   statemodule
*   the hearth of the whole osciloscope
*   TODO shift the memory, so the first sample is on the first place in
*   memmory
*   TODO more advanced trigger logic (external module)
*/ 

module sampler(
	
	input        clk_50mhz, reset,
	
	input        activate, // drive to 1 to activate the module
	output       done,    // signals that the module has done what it needed to do
	
	output       adc_clk,
	input  [7:0] adc_data
	
	output [7:0] mem_data,
	output [7:0] mem_addr,
	output 		 mem_we
	);
	


    reg [SAMPLE_DEPTH<<2:0]   post_samples;  /* 50% trigger placement */
    reg [SAMPLE_DEPTH<<1:0]   offset;

    reg                       active;
    reg                       trig;

    /****** module state watcher ******/
    always @(posedge state_change)
    begin
        if(state == module_id)
            active <= 1;
        else
            active <= 1;

    end

    typedef enum logic[2:0] {
        IDLE,
        SETUP,
        PRE_TRIG,
        POST_TRIG,
        CLEAN
        } sampler_state;
    sampler_state sampler;

    assign clk_adc = clk;

    /****** FSM `*****/
    always @(posedge clk_adc)
        case(sampler_state)
            IDLE: begin
                if(active)
                    sampler_state = SETUP;
            end
            SETUP: begin
                m_we    <= 1;
                m_cs    <= 1;
                m_addr <= 1;
                post_samples <= 0;
                sample_state <= PRE_TRIG;
            end
            /* store samples in memmory and add 1 to address and let it
            * overflow indefinitley (redneck circular-buffer) */
            PRE_TRIG: begin /* pre-tringer */
                mem[m_addr] <= data_in;
                m_addr      <= m_addr+ 1;
                if(trig)
                begin
                    sampler_state <= POST_TRIG;
                    m_offset <= m_addr;
                end
            end
            /* continue to store samples, but also watch for the number of
            * amples, if its more than half of of the buffer, goto next */
            POST_TRIG: begin /* post-trig */
                mem[m_addr] <= data_in;
                m_addr <= m_addr + 1;
                post_samples <= post_samples + 1;
                if(&post_samples)  /* reduction AND */
                    sampler_state <= CLEAN;
            end
            CLEAN: begin
                m_we = 0;
                m_cs = 0;
                sampler_state <= IDLE;
            end
        endcase


    /***** TRIGGER LOGIC *****/
    reg thr1, thr2;
    always @(posedge clk_adc)
    begin
        thr1 <= (data_in >= 8'h80);
        thr2 <= thr1;
    end

    /* assert true for one clock at rising edge */
    assign trig = thr1 & ~thr2;

endmodule
