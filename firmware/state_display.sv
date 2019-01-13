module state_display(
    clk,
    state, state_change,
    segA, segB, segC, segD, segE, segF, segG,
    dsEN
    );

    input            clk;
    output           segA, segB, segC, segD, segE, segF, segG;

    input wire [7:0] state;
    input            state_change;
    output reg [3:0] dsEN;


        /* generate clocksignal for display */
    reg              slow_clock;
    reg [24:0]       counter = 0; /* 50Mhz divided by 2^16 is roughly 760Hz */
    always @(posedge clk)
        begin
            counter = counter+1;
            slow_clock = counter[15];
        end


    reg [3:0]        bcd [3:0];

        /* display instance */
    seven_segment ss(
        .clk (slow_clock),
        .bcd (bcd),
        .segA(segA),
        .segB(segB),
        .segC(segC),
        .segD(segD),
        .segE(segE),
        .segF(segF),
        .segG(segG),
        .dsen(dsEN)
    );

    assign bcd[2] = state[3:0];
    assign bcd[3] = state[7:4];

endmodule
