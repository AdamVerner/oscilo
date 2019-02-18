/*
 * generates ramping signal
 */

module fake_adc(
    input        clk,
    input        rst,
    output [7:0] data_out = 0
    );

    always @(posedge clk)
        begin
            if (~rst)
                data_out = 0;
            else
                begin
                    data_out += 1;
                    if(data_out == 255)
                        data_out = 0;
                end


        end

endmodule