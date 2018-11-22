

module state_display(
    clk,
    state, state_change,
    segReg, dsEN);

    input           clk;

    input reg[7:0]  state;
    input           state_change;

    output reg[7:0] segReg;
    output reg[3:0] dsEN;


    /* generate clocksignal for display */
    reg slow_clock;
    reg[15:0] counter = 0; /* 50Mhz divided by 2^16 is roughly 760Hz */
    always @(posedge clk)
    begin
        counter = counter + 1;
        slow_clock = counter[15];
    end


    reg[3:0]  bcd[3:0];

    /* display instance */
    seven_segment ss(.clk(slow_clock), .bcd(bcd),
    .segA(segReg[0]), .segB(segReg[1]), .segC(segReg[2]),
    .segD(segReg[3]), .segE(segReg[4]), .segF(segReg[5]), .segG(segReg[6]),
    .dsen(dsEN));

    assign bcd[2] = state[3:0];
    assign bcd[3] = state[7:4];

endmodule
