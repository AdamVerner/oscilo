// Testbench
module test;

    reg sclk;
    reg [3:0] data[3:0];

    reg [7:0] leds;
    reg [3:0] dsen;


seven_segment DUT(
    .clk(sclk),
    .bcd(data),
    .segA(leds[0]),
    .segB(leds[1]),
    .segC(leds[2]),
    .segD(leds[3]),
    .segE(leds[4]),
    .segF(leds[5]),
    .segG(leds[6]),
    .dsen(dsen)
    );

    initial begin
        // Dump waves
        $dumpfile("dump.vcd");
        $dumpvars(1);

        sclk = 0;
        #50 data[0] = 8'h8;  // h8 = b11111110
        #50 data[3] = 8'hF;  // hf = 01110001
    end

    always begin
        #1 sclk = ~sclk;
    end


endmodule

