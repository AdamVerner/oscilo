// Testbench
/*
 * I usually don't write testbenches for rams, but as this is school project, ill rather do it...
 *
*/
module test;

    reg clk;
    reg [7:0] addr_in;
    reg [7:0] addr_out;
    reg [7:0] data_in;
    reg [7:0] data_out;
    reg cs, we, oe;

    ram_sw_ar DUT(
    .clk(clk),
    .addr_in(addr_in),
    .addr_out(addr_out),
    .data_in(data_in),
    .data_out(data_out),
    .cs(cs),
    .we(we),
    .oe(oe)
    );


    initial begin
        // Dump waves
        $dumpfile("dump.vcd");
        $dumpvars(1);

        clk = 0;
        cs = 1;
        we = 0;
        oe = 0;

        addr_in = 8'h01;
        data_in = 8'hFA;
        #1 clk = ~clk;
        we = 1;
        addr_in = 8'h02;
        data_in = 8'h7B;
        #1 clk = ~clk;

        #1 oe = 1;
        #1 addr_out = 8'h03; // should be empty;
        #1 addr_out = 8'h01; // should be empty;
        #5 oe = 0;
        #1 addr_out = 8'h01; // should be empty;

    end



endmodule