// replys back bytes till 0x55 is received

module replayer(
    input clk, reset,

    input activate,
    output done,

    input tx_done,
    input rx_ready,
    input rx_data,

    output tx_data,
    output tx_start

);

    reg [2:0] state;

    parameter ST_IDLE   = 0;
    parameter ST_RECV   = 1;
    parameter ST_WAIT   = 2;
    parameter ST_REPLY  = 3;
    parameter ST_DONE   = 4;

    always @(posedge clk)
        case(state)
            ST_IDLE:
            begin
                tx_data  = 8'hz;
                tx_start = 1'bz;
                if(activate)
                    state = ST_RECV;
            end
            ST_RECV:
            begin
                tx_start = 0;
                if(rx_ready)
                begin
                    tx_data = rx_data;
                    state = ST_WAIT;
                end
            end
            ST_WAIT:
                if(~tx_active)
                    state = ST_REPLY;
            ST_REPLY:
            begin
                tx_start = 1;
                if(rx_data == 8'h55)
                    state = ST_DONE;
                else
                    state = ST_RECV;
            end
            ST_DONE:
            begin
                done = 1;
                if(~activate)
                    state = ST_IDLE;
            end
            default:
                state = ST_IDLE;
        endcase

endmodule