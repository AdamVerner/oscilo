module main(

	input CLK, // MAIN 50 MHZ clock
	
	input RXD,   // UART_IN
	input KEY4,  // RESET
	
	output DS_A, DS_B, DS_C, DS_D, DS_E, DS_F, DS_G,
	output DSEN_1, DSEN_2, DSEN_3, DSEN_4 // active LOW
	);
	
	wire [7:0] rx_data;
	wire rx_ready;
	
	wire clk_500hz;
	reg [15:0] dsp_cnt;
	reg [3:0] dsp_en;
	
	
	uart_rx reciever(.clk(CLK), .rxd(RXD), .rx_rd(rx_ready), .rx_data(rx_data));

	seven_segment segmentdisplay(.clk_50mhz(CLK), .reset(KEY4),
								 .bcd1(4'h0), .bcd2(4'h0), .bcd3(rx_data[3:0]), .bcd4(rx_data[7:4]),
								 .segA(DS_A), .segB(DS_B), .segC(DS_C), .segD(DS_D),
								 .segE(DS_E), .segF(DS_F), .segG(DS_G),
								 .dsen1(DSEN_1), .dsen2(DSEN_2), .dsen3(DSEN_3), .dsen4(DSEN_4)
								);

endmodule





