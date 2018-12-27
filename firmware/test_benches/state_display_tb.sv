// Testbench
module test;

    reg [7:0]   state;
    reg         state_change;

    reg [7:0]   leds;       // reflects real hw
    reg [3:0]   cathodes;   // reflects real hw

    reg clk;

    /* DUT */

    state_display DUT(.clk(clk), .state(state), .state_change(state_change),
    .segReg(leds), .dsEN(cathodes));

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(1);
        clk = 0;
        state = 0;
        state_change = 0;

        #100 state = 8'h5A; state_change = 1;
        #1 state_change = 0;

        #100 state = 8'h5A; state_change = 1;
        #1 state_change = 0;

        #100 state = 8'h5A; state_change = 1;
        #1 state_change = 0;

    end



    always begin
        #11 clk = ~clk;
    end



endmodule