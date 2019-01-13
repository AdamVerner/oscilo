module main(

    input        CLK, // MAIN 50 MHZ clock

    input        RXD,   // UART
    output       TXD,

    input        KEY4,  // RESET

    output [7:0] debug,  // test only

    output       DS_A, DS_B, DS_C, DS_D, DS_E, DS_F, DS_G,
    output       DSEN_1, DSEN_2, DSEN_3, DSEN_4 // active LOW
    );

    wire [7:0] rx_data;
    wire       rx_ready;

    wire [7:0] tx_data;
    wire       tx_start, tx_active, tx_done;

    reg [7:0]  state;
    wire       state_change;


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
    ram_sw_ar#(.DATA_WIDTH(8), .ADDR_WIDTH(8)) sample_memmory(
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


    // sampler_instance start
    wire       sampler_activate, sampler_done;
    wire [7:0] adc_data;
    wire       adc_clk;
    fake_adc fake_adc_instance(
        .clk     (adc_clk),
        .rst     (KEY4),
        .data_out(adc_data)
    );
    sampler sampler_instance(
        .clk_50mhz(CLK),
        .reset    (KEY4),
        .activate (sampler_activate),
        .done     (sampler_done),
        .adc_clk  (adc_clk),
        .adc_data (adc_data),
        .mem_data (sm_data_in),
        .mem_addr (sm_addr_in),
        .mem_we   (sm_we),
        .mem_clk  (sm_clk)
    );
    // sampler_instance stop


    // sample_reader_instance start
    wire       sample_reader_activate, sample_reader_done;
    // sample_reader_instance stop


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


    // test instance start
    wire       test_activate, test_done;
    test testinstance(
        .clk_50mhz(CLK),
        .reset    (KEY4),
        .activate (test_activate),
        .done     (test_done),
        .to       (debug[0])
    );
    // test instance end


    // UART_TX MANAGER START
    always @(posedge CLK)
        begin
            if (replayer_activate) begin
                tx_data = replayer_tx_data;
                tx_start = replayer_tx_start;
            end else if (reply_cnt_activate) begin
                tx_data = reply_cnt_tx_data;
                tx_start = reply_cnt_tx_start;
            end else
                tx_start = 0;
        end
    // UART_TX MANAGER START


    // STATE_WATCHER states
    parameter ST_READY = 8'h01;  // just wait one clk cycle
    parameter ST_INIT = 8'h00;
    parameter ST_TEST = 8'h11;
    parameter ST_SAMPLER = 8'h21;
    parameter ST_SAMPLE_READ = 8'h22;
    parameter ST_REPLAYER = 8'h71;
    parameter ST_REPLY_CNT = 8'h72;


    initial begin
        state_change = 0;
        state = ST_INIT;
    end

    always @(posedge CLK)
        begin

            if (~KEY4) //reset
                begin
                    state_change = 0;
                    state = ST_INIT;
                    // no need to specify *_activate signals as they'll get set to zero in next clk run
                end


            if (state_change) // watch for state_change and if changed activate appropriate module
                begin
                    case (state)
                        ST_TEST: test_activate = 1;
                        ST_SAMPLER: sampler_activate = 1;
                        ST_SAMPLE_READ: sample_reader_activate = 1;
                        ST_REPLAYER: replayer_activate = 1;
                        ST_REPLY_CNT: reply_cnt_activate = 1;

                        ST_INIT: // set all activate signals to 0
                            begin
                                test_activate = 0;
                                sampler_activate = 0;
                                sample_reader_activate = 0;
                                replayer_activate = 0;
                                reply_cnt_activate = 0;
                            end
                        ST_READY:
                            if(~rx_ready && ~tx_active)
                            state = ST_INIT;
                    endcase
                end


            if (test_activate && test_done) // watch for module done
                state = ST_INIT;

            if (replayer_activate && replayer_done)
                state = ST_INIT;

            if (sample_reader_activate && sample_reader_done)
                state = ST_INIT;

            if (reply_cnt_activate && reply_cnt_done)
                state = ST_INIT;


            if (rx_ready && state == ST_INIT)  // watch for state_change request
                begin
                    state_change = 1;
                    state = rx_data;
                end else begin
                state_change = 0;
            end

        end

endmodule





