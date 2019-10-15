// Testbench
module test;

  reg  clk;

  reg		Rx_ready;
  reg [7:0]	Rx_data;
  reg 		reset;
  
  reg [7:0]	state;
  reg		state_change;
  
  state_watcher #(8'h15) DUT (
    .Rx_ready(Rx_ready),
    .Rx_data(Rx_data),
    .reset(reset),
    .state(state),
    .state_change(state_change)
  );
  
  
  initial begin
    // Dump waves
    $dumpfile("dump.vcd");
    $dumpvars(1);
    
    Rx_ready = 0;
    Rx_data = 8'h7F;
    reset = 0;
    
    /* module should be active, so first recived byte should be written to state
    * and the the module should be inactive
    */
    #1 Rx_data = 8'hB6;
    #1 Rx_ready = 1;
    #1 Rx_ready = 0;
    
    /* this should be ignore, because the state isnt same as  module id */
    #1 Rx_data = 8'hA7;
    #1 Rx_ready = 1;
    #1 Rx_ready = 0;
    
    /* reset the module to default*/
    #1 reset = 1;
    #1 reset = 0;
    
    /* assign valid state */
    #1 Rx_data = 8'h7a;
    #1 Rx_ready = 1;
    #1 Rx_ready = 0;
    
  end

  task clk;
    #1 clk = ~clk;
    #1 clk = ~clk;

  endtask


endmodule
