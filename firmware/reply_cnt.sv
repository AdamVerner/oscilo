// replys back bytes till 0x55 is received

module reply_cnt(
    input        clk,
                 reset,

    input        activate,
    output       done,

    input        tx_done,
    input        tx_active,
    input        rx_ready,
    input  [7:0] rx_data,

    output [7:0] tx_data,
    output       tx_start
    );

    reg [22:0] sleep_counter;  // max = 8388607

    reg [7:0] count;
    reg [7:0] counter;
    reg [3:0] state;

    parameter ST_IDLE = 0;
    parameter ST_RECV = 1;
    parameter ST_WAIT = 2;
    parameter ST_REPLY = 3;
    parameter ST_DONE = 4;
    parameter ST_INTER = 5;

    always @(posedge clk)
        begin
            if (~reset) state = ST_IDLE;

            case (state)
                ST_IDLE: begin
                    tx_start = 0;
                    done = 0;
                    counter = 0;
                    //when activated wait for RX line to clean from preious state change
                    if (activate & ~rx_ready)
                        state = ST_RECV;
                end
                ST_RECV: begin
                    if (rx_ready)
                        begin
                            count = rx_data;
                            state = ST_WAIT;
                        end
                end
                ST_WAIT: begin
                    tx_start = 0;
                    if (~tx_active)
                        begin
                        state = ST_INTER;
                        sleep_counter = 0;
                        end
                end

                ST_INTER: begin // TODO optimalize sleep times
                    sleep_counter = sleep_counter + 1;
                    if(sleep_counter >= 5000000) // wait 0.1 sec

                        state = ST_REPLY;
                end
                ST_REPLY: begin
                    tx_data = counter;
                    tx_start = 1;

                    counter = counter + 1'b1;

                    if (counter >= count)
                        state = ST_DONE;
                    else
                        state = ST_WAIT;
                end
                ST_DONE: begin
                    done = 1;
                    tx_start = 0;

                    if (~activate & ~rx_ready & ~tx_active)
                        state = ST_IDLE;

                end
                default: state = ST_IDLE;
            endcase
        end
endmodule