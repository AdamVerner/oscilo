/*
 * Single port ram with synchornous write and async read
 * if output enable is low, the data out is in high-Z
 *
 * sourced from.....
 * documentation...
*/
module ram_sw_ar #( parameter DATA_WIDTH = 8,
                    parameter ADDR_WIDTH = 8)(
input   wire                  clk,      // Clock Input
input   wire [ADDR_WIDTH-1:0] addr_in,  // Address Input
input   wire [ADDR_WIDTH-1:0] addr_out, // Address Input
input   wire [DATA_WIDTH-1:0] data_in,  // Data input
output  wire [DATA_WIDTH-1:0] data_out, // Data output
input   wire                  cs,       // Chip Select
input   wire                  we,       // Write Enable
input   wire                  oe        // Output Enable
);


reg [DATA_WIDTH-1:0] mem [ADDR_WIDTH-1:0];


/* Synchronous memmory write */
always @ (posedge clk)
begin
    if ( cs && we ) begin
       mem[addr_in] = data_in;
   end
end

/* Synchronous memmory read */
assign data_out = (cs && oe ) ? mem[addr_out] : {(DATA_WIDTH){1'bz}};

endmodule
