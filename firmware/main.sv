module main(

	input CLK, // MAIN 50 MHZ clock
	
	input RXD,   // UART_IN
	input KEY4,  // RESET
	
	output [7:0] debug,  // test only
	
	output DS_A, DS_B, DS_C, DS_D, DS_E, DS_F, DS_G,
	output DSEN_1, DSEN_2, DSEN_3, DSEN_4 // active LOW
	);
	
	wire [7:0]	rx_data;
	wire 			rx_ready;
	
	reg [7:0] 	state;
	wire			state_change;
	
		
	uart_rx reciever(.clk(CLK), .rxd(RXD), .rx_rd(rx_ready), .rx_data(rx_data));

	seven_segment segmentdisplay(.clk_50mhz(CLK), .reset(KEY4),
								 .bcd1(4'h0), .bcd2(4'h0), .bcd3(state[3:0]), .bcd4(state[7:4]),
								 .segA(DS_A), .segB(DS_B), .segC(DS_C), .segD(DS_D),
								 .segE(DS_E), .segF(DS_F), .segG(DS_G),
								 .dsen1(DSEN_1), .dsen2(DSEN_2), .dsen3(DSEN_3), .dsen4(DSEN_4)
								);
	// sampling memmory start
	wire sm_we, sm_oe;
	wire [7:0] sm_data_in;
	wire [7:0] sm_data_out;
	wire [7:0] sm_addr_in;
	wire [7:0] sm_addr_out;
	ram_sw_ar (.DATA_WIDTH(8), .ADDR_WIDTH(8)) sample_memmory (.clk(CLK), .addr_in(sm_addr_in), .addr_out(sm_addr_out), .data_in(sm_data_in), .data_out(sm_data_out), .cs(1), .we(sm_we), .oe(sm_oe));
	// sampling memmory end
	
	
	// sampler_instance start
	wire sampler_activate, sampler_done;
	wire [7:0] 	adc_data;
	wire			adc_clk;
	fake_adc fake_adc_instance(.clk(adc_clk), .rst(KEY4), .data_out(adc_data));
	sampler sampler_instance(.clk_50mhz(CLK), .reset(KEY4), .activate(sampler_activate), .done(sampler_done), .adc_clk(adc_clk), .adc_data(adc_data), .mem_data(sm_data_in), .mem_addr(sm_addr_in), .mem_we(sm_we));
	// sampler_instance stop
	
	
	// sample_reader_instance start
	
	
	// sample_reader_instance stop
	
	
	
	// test instance start
	wire test_activate, test_done;
	test testinstance(.clk_50mhz(CLK), .reset(KEY4), .activate(test_activate), .done(test_done), .to(debug[0]));
	// test instance end

	// STATE_WATCHER states
	parameter ST_INIT				= 8'h00;
	parameter ST_TEST				= 8'h11;
	parameter ST_SAMPLER			= 8'h21;
	parameter ST_SAMPLE_READ	= 8'h22;
	
	
	initial begin
			state_change = 0;
			state = ST_INIT;
	end
	
	always @(posedge CLK)
	begin
	
		if(~KEY4) //reset
		begin
			state = ST_INIT;
			state_change = 0;
			// no need to specify *_activate signals as they'll get set to zero in next clk run
		end
	
		
		if(state_change) // watch for state_change and if changed activate appropriate module
		begin
			case(state)
				ST_TEST: 			test_activate = 1;
				ST_SAMPLER:			sampler_activate = 1;
				ST_SAMPLE_READ:	sample_reader_activate = 1;
				
				default: // set all activate signals to 0
					test_activate = 0;
					sampler_activate = 0;
					sample_reader_activate = 0;
			endcase
		end
		
		
		if(test_activate && test_done) // watch for module done
			state = ST_INIT;

		if(rx_ready && state == ST_INIT)  // watch for state_change request
		begin
			state_change = 1;
			state = rx_data;
		end else begin
			state_change = 0;
		end
	
	
	end				
								
endmodule





