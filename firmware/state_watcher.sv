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

    parameter [7:0] module_id = 8'h00;

    input             Rx_ready;
    input       [7:0] Rx_data;
    input             reset;

    output wire [7:0] state;
    output            state_change;

    reg [7:0]         state_temp;
    reg               state_change_temp;

    assign state_change = state_change_temp;
    assign state = state_temp;




    always @(negedge Rx_ready)
        state_change_temp <= 0;


endmodule
