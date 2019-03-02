module main(

    input        CLK, // MAIN 50 MHZ clock

    input        RXD,   // UART
    output       TXD,

    input        KEY4,  // RESET

    input        KEY3,  // FORCE_TRIGGER

    output       DS_A, DS_B, DS_C, DS_D, DS_E, DS_F, DS_G,
    output       DSEN_1, DSEN_2, DSEN_3, DSEN_4, // active LOW
    output       LED_GREEN, LED_RED
    );

    wire [7:0] rx_data;
    wire       rx_ready;

    wire [7:0] tx_data;
    wire       tx_start, tx_active, tx_done;

    reg [7:0]  state;


    parameter SAMPLE_DEPTH = 8;   /* max adress is (1 << SAMPLE_DEPTH)-1 */


    uart_rx reciever(
        .clk    (CLK),
        .rxd    (RXD),
        .rx_rd  (rx_ready),
        .rx_data(rx_data)
    );

    uart_tx transmiter(
        .clk   (CLK),
        .txd   (TXD),
        .start (tx_start),
        .data  (tx_data),
        .active(tx_active),
        .done  (tx_done)
    );

    seven_segment segmentdisplay(
        .clk_50mhz(CLK),
        .reset    (KEY4),
        .bcd1     (4'h0),
        .bcd2     (4'h0),
        .bcd3     (state[3:0]),
        .bcd4     (state[7:4]),
        .segA     (DS_A),
        .segB     (DS_B),
        .segC     (DS_C),
        .segD     (DS_D),
        .segE     (DS_E),
        .segF     (DS_F),
        .segG     (DS_G),
        .dsen1    (DSEN_1),
        .dsen2    (DSEN_2),
        .dsen3    (DSEN_3),
        .dsen4    (DSEN_4)
    );

    // sampling memmory start
    wire       sm_we, sm_oe, sm_clk;
    wire [7:0] sm_data_in;
    wire [7:0] sm_data_out;
    wire [7:0] sm_addr_in;
    wire [7:0] sm_addr_out;
    ram_sw_ar#(.DATA_WIDTH(8), .ADDR_WIDTH(SAMPLE_DEPTH)) sample_memmory(
        .clk     (sm_clk),
        .addr_in (sm_addr_in),
        .addr_out(sm_addr_out),
        .data_in (sm_data_in),
        .data_out(sm_data_out),
        .cs      (1),
        .we      (sm_we),
        .oe      (sm_oe)
    );
    // sampling memmory end


    // mem clearer start
    wire       mem_clear_activate, mem_clear_done;
    wire [7:0] mem_clear_data_in;
    wire [SAMPLE_DEPTH-1:0] mem_clear_addr_in;
    wire       mem_clear_we;
    wire       mem_clear_clk;
    mem_clear #(.SAMPLE_DEPTH(SAMPLE_DEPTH)) mem_clear_instance(
      .clk_50mhz(CLK),
      .reset    (KEY4),
      .activate (mem_clear_activate),
      .done     (mem_clear_done),
      .rx_data  (rx_data),
      .rx_ready (rx_ready),
      .mem_clk  (mem_clear_clk),
      .mem_data (mem_clear_data_in),
      .mem_addr (mem_clear_addr_in),
      .mem_we   (mem_clear_we)
    );
    // mem clear stop


    // trigger  and trigger configurator start
    wire trig_config_activate, trig_config_done;
    wire [7:0] upper_bound, lower_bound;
    wire en_rise, en_fall;
    trig_config trig_config_instance(
        .clk(CLK),
        .rst(KEY4),
        .activate(trig_config_activate),
        .done(trig_config_done),
        .rx_data(rx_data),
        .rx_ready(rx_ready),
        .upper_bound(upper_bound),
        .lower_bound(lower_bound),
        .en_rise(en_rise),
        .en_fall(en_fall)
    );
    wire                    trig_rst, trig;
    trigger #(.WIDTH(8)) trigger_instance(
        .rst(KEY4),
        .clk(adc_clk),   // wire it parallel to sampler
        .data(adc_data),
        .trig_rst(trig_rst),
        .upper_bound(upper_bound),
        .lower_bound(lower_bound),
        .en_rise(en_rise),
        .en_fall(en_fall),
        .trigger(trig)
    );
    // trigger  and trigger configurator stop



    // sampler_instance start
    assign LED_GREEN = sampler_activate;
    assign LED_RED = sampler_done;
    wire                    sampler_activate, sampler_done;
    wire [7:0]              adc_data;
    wire                    adc_clk;
    wire [7:0]              sampler_data_in;
    wire                    sampler_we;
    wire                    sampler_clk;
    wire [SAMPLE_DEPTH-1:0] sampler_addr_in;
    wire [SAMPLE_DEPTH-1:0] offset;
    wire [7:0]              sampler_tx_data;
    wire                    sampler_tx_start;
    sampler #(.SAMPLE_DEPTH(SAMPLE_DEPTH)) sampler_instance(
        .clk_50mhz (CLK),
        .reset     (KEY4),
        .activate  (sampler_activate),
        .done      (sampler_done),
        .adc_clk   (adc_clk),
        .adc_data  (adc_data),
        .mem_data  (sampler_data_in),
        .mem_addr  (sampler_addr_in),
        .mem_we    (sampler_we),
        .mem_clk   (sampler_clk),
        .offset    (offset),
        .force_trig(~KEY3),
        .trig      (trig),
        .trig_reset(trig_rst),
        .clk_div   (clk_division),
        .tx_active (tx_active),
        .tx_data   (sampler_tx_data),
        .tx_start  (sampler_tx_start),
        .rx_data   (rx_data),
        .rx_ready  (rx_ready)
    );
    wire                    clk_cfg_activate, clk_cfg_done;
    wire [15:0]             clk_division;
    sample_clock_config sample_clock_config_instance(
        .clk     (CLK),
        .rst     (KEY4),
        .activate(clk_cfg_activate),
        .done    (clk_cfg_done),
        .rx_data (rx_data),
        .rx_ready(rx_ready),
        .clk_div (clk_division)
    );
    // sampler_instance stop


    // sample_reader_instance start
    wire                    sample_reader_activate, sample_reader_done;
    wire [7:0]              sampler_reader_tx_data;
    wire                    sampler_reader_tx_start;
    wire                    sample_reader_oe;
    wire [SAMPLE_DEPTH-1:0] sample_reader_addr_out;
    sample_reader #(.SAMPLE_DEPTH(SAMPLE_DEPTH)) sample_reader_instace(
        .clk_50mhz(CLK),
        .reset(KEY4),
        .activate(sample_reader_activate),
        .done(sample_reader_done),
        .tx_active(tx_active),
        .tx_data(sampler_reader_tx_data),
        .tx_start(sampler_reader_tx_start),
        .mem_data(sm_data_out),
        .mem_addr(sample_reader_addr_out),
        .mem_oe(sample_reader_oe)
    );
    // sample_reader_instance stop


    // adc selector start
        // first ADC
        wire       first_adc_clk;
        wire [7:0] first_adc_data;
        fake_adc #(
            .WIDTH(8),
            .INC(1),
            .DEC(1)) first_fake(
            .clk     (CLK),
            .rst     (KEY4),
            .data_out(first_adc_data)
        );
        // second ADC
        wire       second_adc_clk;
        wire [7:0] second_adc_data;
        fake_adc #(
            .WIDTH(8),
            .INC(5),
            .DEC(5)) second_fake( .clk(second_adc_clk), .rst(KEY4), .data_out(second_adc_data) );
        // third ADC
        wire       third_adc_clk;
        wire [7:0] third_adc_data;
        fake_adc #(
            .WIDTH(8),
            .INC(1),
            .DEC(1)) third_fake(
            .clk     (third_adc_clk),
            .rst     (KEY4),
            .data_out(third_adc_data)
        );

    wire selector_done, selector_activate;
    adc_selector adc_selector_instance(
        .clk      (CLK),
        .rst      (KEY4),
        .activate (selector_activate),
        .done     (selector_done),
        .rx_data  (rx_data),
        .rx_ready (rx_ready),
        .adc1_data(first_adc_data),
        .adc1_clk (first_adc_clk),
        .adc2_data(second_adc_data),
        .adc2_clk (second_adc_clk),
        .adc3_data(third_adc_data),
        .adc3_clk (third_adc_clk),
        .adc_data (adc_data),
        .adc_clk  (adc_clk),
    );
    // adc selector stop


    // last offset getter start
    wire       sample_offset_activate, sample_offset_done;
    wire [7:0] sample_offset_tx_data;
    wire       sample_offset_tx_start;
    sample_offset #(.SAMPLE_DEPTH(SAMPLE_DEPTH)) sample_offset_instance(
        .clk_50mhz(CLK),
        .reset(KEY4),
        .activate(sample_offset_activate),
        .done(sample_offset_done),
        .tx_active(tx_active),
        .tx_data(sample_offset_tx_data),
        .tx_start(sample_offset_tx_start),
        .offset(offset)
    );
    // last offset getter stop


    // replayer_instance start
    wire       replayer_activate, replayer_done;
    wire [7:0] replayer_tx_data, replayer_tx_start;
    replayer replayer_instance(
        .clk      (CLK),
        .reset    (KEY4),
        .activate (replayer_activate),
        .done     (replayer_done),
        .tx_done  (tx_done),
        .rx_ready (rx_ready),
        .rx_data  (rx_data),
        .tx_data  (replayer_tx_data),
        .tx_start (replayer_tx_start),
        .tx_active(tx_active)
    );
    // replayer_instance stop


    // reply_cnt_instance start
    wire       reply_cnt_activate, reply_cnt_done;
    wire [7:0] reply_cnt_tx_data, reply_cnt_tx_start;
    reply_cnt reply_cnt_instance(
        .clk      (CLK),
        .reset    (KEY4),
        .activate (reply_cnt_activate),
        .done     (reply_cnt_done),
        .tx_done  (tx_done),
        .rx_ready (rx_ready),
        .rx_data  (rx_data),
        .tx_data  (reply_cnt_tx_data),
        .tx_start (reply_cnt_tx_start),
        .tx_active(tx_active)
    );
    // reply_cnt_instance stop


    // MEDIA MANAGER START
    always @(posedge CLK)
        begin
            if (replayer_activate) begin
                tx_data = replayer_tx_data;
                tx_start = replayer_tx_start;
            end else if (reply_cnt_activate) begin
                tx_data = reply_cnt_tx_data;
                tx_start = reply_cnt_tx_start;
            end else if (sample_reader_activate) begin
                tx_data = sampler_reader_tx_data;
                tx_start = sampler_reader_tx_start;
            end else if (sample_offset_activate) begin
                tx_data = sample_offset_tx_data;
                tx_start = sample_offset_tx_start;
            end else if (sampler_activate) begin
                tx_data = sampler_tx_data;
                tx_start = sampler_tx_start;
            end else
                tx_start = 0;
        end

    assign sm_we =  (sampler_we  && sampler_activate) | (mem_clear_we  && mem_clear_activate);
    assign sm_clk = (sampler_clk && sampler_activate) | (mem_clear_clk && mem_clear_activate);

    assign sm_data_in = (sampler_data_in   & {8{sampler_activate}}) |
                        (mem_clear_data_in & {8{mem_clear_activate}});

    assign sm_addr_in = (sampler_addr_in   & {8{sampler_activate}}) |
                        (mem_clear_addr_in & {8{mem_clear_activate}});

    assign sm_addr_out = (sample_reader_addr_out & {8{sample_reader_activate}});

    assign sm_oe =       (sample_reader_oe && sample_reader_activate);
    // MEDIA MANAGER STOP


    // STATE_WATCHER states
    parameter ST_READY = 8'h01;  // just wait one clk cycle
    parameter ST_INIT = 8'h00;

    parameter ST_SAMPLER = 8'h21;
    parameter ST_SAMPLE_READ = 8'h22;
    parameter ST_MEM_CLEAR = 8'h23;
    parameter ST_OFFSET_GETTER = 8'h24;
    parameter ST_ADC_SELECTOR = 8'h25;

    parameter ST_TRIG_CONFIG = 8'h31;
    parameter ST_CLK_CFG = 8'h32;

    parameter ST_REPLAYER = 8'h71;
    parameter ST_REPLY_CNT = 8'h72;


    initial begin
        state = ST_INIT;
    end

    always @(posedge CLK)
        begin

            if (~KEY4) //reset
                begin
                    state = ST_READY;
                    // no need to specify *_activate signals as they'll get set to zero in next clk run
                end

            case (state)
                ST_SAMPLER: sampler_activate = 1;
                ST_SAMPLE_READ: sample_reader_activate = 1;
                ST_REPLAYER: replayer_activate = 1;
                ST_REPLY_CNT: reply_cnt_activate = 1;
                ST_MEM_CLEAR: mem_clear_activate = 1;
                ST_OFFSET_GETTER: sample_offset_activate = 1;
                ST_ADC_SELECTOR: selector_activate = 1;
                ST_TRIG_CONFIG: trig_config_activate = 1;
                ST_CLK_CFG: clk_cfg_activate = 1;

                ST_INIT:
                    if(rx_ready)
                        state = rx_data;

                ST_READY:
                begin
                    sampler_activate = 0;
                    sample_reader_activate = 0;
                    replayer_activate = 0;
                    reply_cnt_activate = 0;
                    mem_clear_activate = 0;
                    sample_offset_activate = 0;
                    selector_activate = 0;
                    trig_config_activate = 0;
                    clk_cfg_activate = 0;

                    if(~rx_ready && ~tx_active)
                    state = ST_INIT;
                end
            endcase

            if (sampler_activate && sampler_done)
                state = ST_READY;

            if (replayer_activate && replayer_done)
                state = ST_READY;

            if (sample_reader_activate && sample_reader_done)
                state = ST_READY;

            if (reply_cnt_activate && reply_cnt_done)
                state = ST_READY;

            if (mem_clear_activate && mem_clear_done)
                state = ST_READY;

            if (sample_offset_activate && sample_offset_done)
                state = ST_READY;

            if (selector_activate && selector_done)
                state = ST_READY;

            if (trig_config_activate && trig_config_done)
                state = ST_READY;

            if (clk_cfg_activate && clk_cfg_done)
                state = ST_READY;


        end

endmodule
