/*
 * watches for incomming traffic, if the module is active writes the incomming byte to state and flips state_change to 1 (should generate posedge)
 * this is the only module that should be default ON
 * TODO add $display(""); for simulations
*/

module state_watcher(
	/* inputs */
	Rx_ready, Rx_data, reset
	/* outputs */
	state, state_change
	);

	parameter [7:0]	module_id = 8'h00;

	input		Rx_ready;
	input [7:0]	Rx_data;
	input 		reset;
	
	output reg[7:0]	state;
	output reg	state_change;

	reg		active;

	task tskReset;
	begin
		state <= module_id;  /* this module should be DEFAULT ON */
		state_change <= 1'b0;
		active <= 1'b0;
	end
	endtask

	initial tskReset();
	always @(posedge reset) tskReset();

	/* TODO is reset posedge or negedge? */
	always @(posedge Rx_ready)
	begin
		if((state == module_id) && active)
		begin
			state <= Rx_data;
			state_change <= 1;
			active <= 0;
		end
		else
			state_change <= 0;
	end

endmodule
