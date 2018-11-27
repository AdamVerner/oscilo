/*
*   statemodule
*   the hearth of the whole osciloscope
*
*/

module sampler #(
    parameter module_id = 8'h10,
    parameter SAMPLE_DEPTH = 1024)(

    /* general signals */
    input   wire        clk,
    input   wire        state,
    input   wire [7:0]  state_change,

    /* ADC */
    input wire [7:0]    data_in,
    output wire         clk_adc,

    /* MEMMORY */
    output              m_clk,
    output              m_addr,
    output              m_we, /* write-enable */
    output              m_cs /* chip-select */
    );


    reg [SAMPLE_DEPTH<<1/2:0] post_samples;  /* 50% trigger placement */
    reg [SAMPLE_DEPTH<<1:0]   offset;

    reg                    trig;

    typedef enum logic[1:0] {
        IDLE,
        PRE_TRIG,
        POST_TRIG,
        CLEAN
        } sampler_state;
    sampler_state sampler;

    assign clk_adc = clk;

    always @(posedge clk_adc)
        case(sampler)
            IDLE: begin /* init */
                m_addr <= 0;
                trig <= 0;
                post_samples <= 0;
                if(active)
                    faze = 1;
            end
            PRE_TRIG: begin /* pre-tring */
                mem[m_addr] <= data_in;
                m_addr <= m_addr+ 1;
                if(trig)
                begin
                    faze <= 2'b10;
                    offset <= m_addr;;
                end
            end
            POST_TRIG: begin /* post-trig */
                mem[m_addr] <= data_in;
                m_addr <= m_addr+ 1;
                post_samples <= post_samples + 1;
                if(&post_samples)  /* reduction AND */
                    faze <= 2'b11;
            end
            CLEAN: begin
            end
        endcase


    /***** TRIGGER LOGIC *****/
    reg thr1, thr2, trig;
    always @(posedge clk_adc)
    begin
        thr1 <= (data_in >= 8'h80);
        thr2 <= thr1;
    end

    /* assert true for one clock at rising edge */
    assign trig = thr1 & ~thr2;





endmodule
