/*
 * generates ramping signal
 */

module fake_adc(
    input              clk, rst,
    output [WIDTH-1:0] data_out
    );

    parameter WIDTH = 8;
    parameter INC = 1;
    parameter DEC = 1;

    reg [WIDTH:0] stage_data = 0;  // one bit bigger, for securing overflows

    parameter maxsize = (1<<WIDTH)-1;
    parameter halfsize = (1<<WIDTH-1)-1;

    assign data_out = stage_data - halfsize;

    reg [1:0] adc_state;
    parameter ST_INC = 0;
    parameter ST_DEC = 1;

    always @(posedge clk)
        begin
            if (~rst)
                stage_data = halfsize;
            else begin
                case(adc_state)
                    ST_INC: begin
                        stage_data += INC;
                        if(stage_data >= (maxsize + halfsize))
                            adc_state = ST_DEC;
                    end
                    ST_DEC: begin
                        stage_data -= DEC;
                        if (stage_data <= halfsize)
                            adc_state = ST_INC;
                    end
                    default: begin
                        stage_data = halfsize;
                        adc_state = ST_INC;
                    end
                endcase
            end
        end

endmodule