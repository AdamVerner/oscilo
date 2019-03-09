/*
 *  if count is 0 the clock stays the same
 *  if it's above zero, the clock is divided `count` times.
 *  does self reset when count changes
 */

module divider(
    input        clk,
    input [15:0] count,
    output       out_clk
);

    reg [15:0] old_count;
    reg [16:0] counter = 0;
    reg        oclk = 1;
    reg        en_thr = 0;

    assign out_clk = en_thr ? clk: oclk;

    always @(posedge clk)
        begin
            if (count >= 1) begin
                en_thr = 0;
                counter = counter+1;
                if (counter == count) begin
                    counter = 0;
                    oclk = ~oclk;
                end
            end else
                en_thr = 1;

            if (old_count != count) begin
                counter = 0;
                oclk = 1;
            end
            old_count = count;

        end

endmodule