/*
 * generates ramping signal
 */

module fake_adc(
				input         clk,
				input         rst,
				output [7:0] data_out,
				);

initial begin
data_out = 0;


always @(posedge clk)
begin
	if(~rst)
		data_out = 0;		
	else
		data_out += 1;

end

endmodule