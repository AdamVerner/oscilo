/*
 * bcd1-4 are indexed from right(1 is LSB in dec)
 * ".bcd1(4'h1), .bcd2(4'h2), .bcd3(4'h3), .bcd4(4'h4)" will result into 4321 on display
 * can print anything from zero to F
 *
 */

module seven_segment(
    input       clk_50mhz,
                reset,

    input [3:0] bcd1,
    input [3:0] bcd2,
    input [3:0] bcd3,
    input [3:0] bcd4,

    output      segA,
                segB,
                segC,
                segD,
                segE,
                segF,
                segG,
    output      dsen1,
                dsen2,
                dsen3,
                dsen4
);


    wire       clk_500hz;
    reg [15:0] dsp_cnt;  // TODO optimalize
    reg [3:0]  dsp_en;
    reg [6:0]  dp_enc [3:0];

    assign {dsen1, dsen2, dsen3, dsen4} = dsp_en;


        // encode input bcd
    always @*
        begin
            case (bcd1)
                4'h0: dp_enc[0] = 7'b1111110;
                4'h1: dp_enc[0] = 7'b0110000;
                4'h2: dp_enc[0] = 7'b1101101;
                4'h3: dp_enc[0] = 7'b1111001;
                4'h4: dp_enc[0] = 7'b0110011;
                4'h5: dp_enc[0] = 7'b1011011;
                4'h6: dp_enc[0] = 7'b1011111;
                4'h7: dp_enc[0] = 7'b1110000;
                4'h8: dp_enc[0] = 7'b1111111;
                4'h9: dp_enc[0] = 7'b1111011;
                4'ha: dp_enc[0] = 7'b1110111;
                4'hb: dp_enc[0] = 7'b0011111;
                4'hc: dp_enc[0] = 7'b1001110;
                4'hd: dp_enc[0] = 7'b0111101;
                4'he: dp_enc[0] = 7'b1001111;
                4'hf: dp_enc[0] = 7'b1000111;
            endcase
            case (bcd2)
                4'h0: dp_enc[1] = 7'b1111110;
                4'h1: dp_enc[1] = 7'b0110000;
                4'h2: dp_enc[1] = 7'b1101101;
                4'h3: dp_enc[1] = 7'b1111001;
                4'h4: dp_enc[1] = 7'b0110011;
                4'h5: dp_enc[1] = 7'b1011011;
                4'h6: dp_enc[1] = 7'b1011111;
                4'h7: dp_enc[1] = 7'b1110000;
                4'h8: dp_enc[1] = 7'b1111111;
                4'h9: dp_enc[1] = 7'b1111011;
                4'ha: dp_enc[1] = 7'b1110111;
                4'hb: dp_enc[1] = 7'b0011111;
                4'hc: dp_enc[1] = 7'b1001110;
                4'hd: dp_enc[1] = 7'b0111101;
                4'he: dp_enc[1] = 7'b1001111;
                4'hf: dp_enc[1] = 7'b1000111;
            endcase
            case (bcd3)
                4'h0: dp_enc[2] = 7'b1111110;
                4'h1: dp_enc[2] = 7'b0110000;
                4'h2: dp_enc[2] = 7'b1101101;
                4'h3: dp_enc[2] = 7'b1111001;
                4'h4: dp_enc[2] = 7'b0110011;
                4'h5: dp_enc[2] = 7'b1011011;
                4'h6: dp_enc[2] = 7'b1011111;
                4'h7: dp_enc[2] = 7'b1110000;
                4'h8: dp_enc[2] = 7'b1111111;
                4'h9: dp_enc[2] = 7'b1111011;
                4'ha: dp_enc[2] = 7'b1110111;
                4'hb: dp_enc[2] = 7'b0011111;
                4'hc: dp_enc[2] = 7'b1001110;
                4'hd: dp_enc[2] = 7'b0111101;
                4'he: dp_enc[2] = 7'b1001111;
                4'hf: dp_enc[2] = 7'b1000111;
            endcase
            case (bcd4)
                4'h0: dp_enc[3] = 7'b1111110;
                4'h1: dp_enc[3] = 7'b0110000;
                4'h2: dp_enc[3] = 7'b1101101;
                4'h3: dp_enc[3] = 7'b1111001;
                4'h4: dp_enc[3] = 7'b0110011;
                4'h5: dp_enc[3] = 7'b1011011;
                4'h6: dp_enc[3] = 7'b1011111;
                4'h7: dp_enc[3] = 7'b1110000;
                4'h8: dp_enc[3] = 7'b1111111;
                4'h9: dp_enc[3] = 7'b1111011;
                4'ha: dp_enc[3] = 7'b1110111;
                4'hb: dp_enc[3] = 7'b0011111;
                4'hc: dp_enc[3] = 7'b1001110;
                4'hd: dp_enc[3] = 7'b0111101;
                4'he: dp_enc[3] = 7'b1001111;
                4'hf: dp_enc[3] = 7'b1000111;
            endcase
        end


        // generate slow clock
    always @(posedge clk_50mhz)
        begin
            dsp_cnt <= dsp_cnt+1;
            if (dsp_cnt == 50000)
                begin
                    dsp_cnt <= 0;
                    clk_500hz <= ~clk_500hz;
                end
        end


        // write to display
    always @(posedge clk_500hz)
        case (dsp_en)
            4'b1110: // rightmost
                begin
                    dsp_en = 4'b1101;
                    {segA, segB, segC, segD, segE, segF, segG} = dp_enc[1];
                end
            4'b1101:
                begin
                    dsp_en = 4'b1011;
                    {segA, segB, segC, segD, segE, segF, segG} = dp_enc[2];
                end
            4'b1011:
                begin
                    dsp_en = 4'b0111;
                    {segA, segB, segC, segD, segE, segF, segG} = dp_enc[3];
                end
            4'b0111: //leftmost
                begin
                    dsp_en = 4'b1110;
                    {segA, segB, segC, segD, segE, segF, segG} = dp_enc[0];
                end
            default:
                dsp_en = 4'b1110;
        endcase

endmodule
