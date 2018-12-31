module test(
	input clk_50mhz, reset,

	input activate, // drive to 1 to activate the module
	output done,    // signals that the module has done what it needed to do
	output to	    // test-out
	);
	
	reg 			act 	= 0;            // active(should be inversion of done)
	reg [25:0]	cnt;
	reg [3:0]	ccls 	= 0;
	reg 			tmp 	= 0;
	
	assign to = tmp;
	
	always @(posedge clk_50mhz)
	begin
	
		if(~reset | ~activate)
		begin
			done  <= 0;
			act   <= 0;
			cnt   <= 0;
			tmp   <= 0;
			ccls  <= 0;
			tmp   <= 0;
		end
		
		if(activate)
			act <= 1;
		
		if(act)
		begin
			cnt <= cnt + 1;
			if(cnt == 50000000)
			begin
				ccls <= ccls + 1;
				cnt <= 0;
				tmp <= ~tmp;
			end
			if(ccls == 10)
			begin
				done <= 1;
				act <= 0;
			end
			
		end
			
	end
			
endmodule
