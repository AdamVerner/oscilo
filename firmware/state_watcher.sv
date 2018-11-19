/*
 * watches for incomming traffic, if the module is active writes the incomming byte to state and flips state_change to 1 (should generate posedge)
 * the state change is controlled by Rx_ready signal, but hta tshould be good, because we only care about the posedge
 * this is the only module that should be default ON
 * TODO add $display(""); for simulations
 * TODO add parametr for controlling of default state(ON/OFF)
*/

module state_watcher(
	/* inputs */
	Rx_ready, Rx_data, reset,
	/* outputs */
	state, state_change
	);

	parameter [7:0]	module_id = 8'h00;

	input		Rx_ready;
	input [7:0]	Rx_data;
	input 		reset;
	
	output reg[7:0]	state;
	output reg	state_change;

	task tskReset;
	begin
		state <= module_id;  /* this module should be DEFAULT ON */
		state_change <= 1'b0;
	end
	endtask

	initial tskReset();
	always @(posedge reset) tskReset();

	/* TODO is reset posedge or negedge? */
	always @(posedge Rx_ready)
	begin
		if((state == module_id))
		begin
			state <= Rx_data;
			state_change <= 1;
		end
	end

	always @(negedge Rx_ready)
		state_change <= 0;
	

endmodule
