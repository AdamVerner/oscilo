/*
* clk signal is something between 100Hz and "few kilos"
* doesn't support the dots between numbers
*/

module seven_segment(
    clk, bcd,
    segA, segB, segC, segD, segE, segF, segG,
    dsen
    );

    input           clk;
    input reg[3:0]  bcd[3:0];

    output          segA, segB, segC, segD, segE, segF, segG;
    output reg[3:0] dsen;

    reg [3:0] faze;
    reg [7:0] SevenSeg;

    initial begin
        faze = 1;
    end


    always @(posedge clk)
    begin
   
        segA <= SevenSeg[6];
        segB <= SevenSeg[5];
        segC <= SevenSeg[4];
        segD <= SevenSeg[3];
        segE <= SevenSeg[2];
        segF <= SevenSeg[1];
        segG <= SevenSeg[0];

        case(faze)
            8'h0: begin
                faze <= 1;
                dsen <= 4'b0001;
            end 8'h1: begin
                faze <= 2;
                dsen <= 4'b0010;
            end 8'h2: begin
                faze <= 3;
                dsen <= 4'b0100;
            end 8'h3: begin
                faze <= 0;
                dsen <= 4'b1000;
            end default: faze <= 0;
        endcase
        case(bcd[faze])
            4'h0: SevenSeg = 8'b11111100;
            4'h1: SevenSeg = 8'b01100000;
            4'h2: SevenSeg = 8'b11011010;
            4'h3: SevenSeg = 8'b11110010;
            4'h4: SevenSeg = 8'b01100110;
            4'h5: SevenSeg = 8'b10110110;
            4'h6: SevenSeg = 8'b10111110;
            4'h7: SevenSeg = 8'b11100000;
            4'h8: SevenSeg = 8'b11111110;
            4'h9: SevenSeg = 8'b11110110;
            4'ha: SevenSeg = 8'b01110111;
            4'hb: SevenSeg = 8'b01111100;
            4'hc: SevenSeg = 8'b00111001;
            4'hd: SevenSeg = 8'b01011110;
            4'he: SevenSeg = 8'b01111001;
            4'hf: SevenSeg = 8'b01110001;
            default: SevenSeg = 8'b00000000;
        endcase

    end


endmodule
