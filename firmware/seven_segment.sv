/*
 * bcd1-4 are indexed from right(1 is LSB in dec)
 * ".bcd1(4'h1), .bcd2(4'h2), .bcd3(4'h3), .bcd4(4'h4)" will result into 4321 on display
 * can print anything from zero to F
 *
 */

module seven_segment(
    input clk_50mhz, reset,

    input [3:0] bcd1,
    input [3:0] bcd2,
    input [3:0] bcd3,
    input [3:0] bcd4,

    output segA, segB, segC, segD, segE, segF, segG,
    output dsen1, dsen2, dsen3, dsen4
    );


    wire clk_500hz;
    reg [15:0] dsp_cnt;  // TODO optimalize
    reg [3:0] dsp_en;
    reg [6:0] dp_enc [3:0];

    assign {dsen1, dsen2, dsen3, dsen4} = dsp_en;


    // encode input bcd
    always @*
    begin
        case(bcd1)
            4'h0: dp_enc[0] = 7'bzzzzzz0;
            4'h1: dp_enc[0] = 7'b0zz0000;
            4'h2: dp_enc[0] = 7'bzz0zz0z;
            4'h3: dp_enc[0] = 7'bzzzz00z;
            4'h4: dp_enc[0] = 7'b0zz00zz;
            4'h5: dp_enc[0] = 7'bz0zz0zz;
            4'h6: dp_enc[0] = 7'bz0zzzzz;
            4'h7: dp_enc[0] = 7'bzzz0000;
            4'h8: dp_enc[0] = 7'bzzzzzzz;
            4'h9: dp_enc[0] = 7'bzzzz0zz;
            4'ha: dp_enc[0] = 7'bzzz0zzz;
            4'hb: dp_enc[0] = 7'b00zzzzz;
            4'hc: dp_enc[0] = 7'bz00zzz0;
            4'hd: dp_enc[0] = 7'b0zzzz0z;
            4'he: dp_enc[0] = 7'bz00zzzz;
            4'hf: dp_enc[0] = 7'bz000zzz;
        endcase
        case(bcd2)
            4'h0: dp_enc[1] = 7'bzzzzzz0;
            4'h1: dp_enc[1] = 7'b0zz0000;
            4'h2: dp_enc[1] = 7'bzz0zz0z;
            4'h3: dp_enc[1] = 7'bzzzz00z;
            4'h4: dp_enc[1] = 7'b0zz00zz;
            4'h5: dp_enc[1] = 7'bz0zz0zz;
            4'h6: dp_enc[1] = 7'bz0zzzzz;
            4'h7: dp_enc[1] = 7'bzzz0000;
            4'h8: dp_enc[1] = 7'bzzzzzzz;
            4'h9: dp_enc[1] = 7'bzzzz0zz;
            4'ha: dp_enc[1] = 7'bzzz0zzz;
            4'hb: dp_enc[1] = 7'b00zzzzz;
            4'hc: dp_enc[1] = 7'bz00zzz0;
            4'hd: dp_enc[1] = 7'b0zzzz0z;
            4'he: dp_enc[1] = 7'bz00zzzz;
            4'hf: dp_enc[1] = 7'bz000zzz;
        endcase
        case(bcd3)
            4'h0: dp_enc[2] = 7'bzzzzzz0;
            4'h1: dp_enc[2] = 7'b0zz0000;
            4'h2: dp_enc[2] = 7'bzz0zz0z;
            4'h3: dp_enc[2] = 7'bzzzz00z;
            4'h4: dp_enc[2] = 7'b0zz00zz;
            4'h5: dp_enc[2] = 7'bz0zz0zz;
            4'h6: dp_enc[2] = 7'bz0zzzzz;
            4'h7: dp_enc[2] = 7'bzzz0000;
            4'h8: dp_enc[2] = 7'bzzzzzzz;
            4'h9: dp_enc[2] = 7'bzzzz0zz;
            4'ha: dp_enc[2] = 7'bzzz0zzz;
            4'hb: dp_enc[2] = 7'b00zzzzz;
            4'hc: dp_enc[2] = 7'bz00zzz0;
            4'hd: dp_enc[2] = 7'b0zzzz0z;
            4'he: dp_enc[2] = 7'bz00zzzz;
            4'hf: dp_enc[2] = 7'bz000zzz;
        endcase
        case(bcd4)
            4'h0: dp_enc[3] = 7'bzzzzzz0;
            4'h1: dp_enc[3] = 7'b0zz0000;
            4'h2: dp_enc[3] = 7'bzz0zz0z;
            4'h3: dp_enc[3] = 7'bzzzz00z;
            4'h4: dp_enc[3] = 7'b0zz00zz;
            4'h5: dp_enc[3] = 7'bz0zz0zz;
            4'h6: dp_enc[3] = 7'bz0zzzzz;
            4'h7: dp_enc[3] = 7'bzzz0000;
            4'h8: dp_enc[3] = 7'bzzzzzzz;
            4'h9: dp_enc[3] = 7'bzzzz0zz;
            4'ha: dp_enc[3] = 7'bzzz0zzz;
            4'hb: dp_enc[3] = 7'b00zzzzz;
            4'hc: dp_enc[3] = 7'bz00zzz0;
            4'hd: dp_enc[3] = 7'b0zzzz0z;
            4'he: dp_enc[3] = 7'bz00zzzz;
            4'hf: dp_enc[3] = 7'bz000zzz;
        endcase
    end


    // generate slow clock
    always @(posedge clk_50mhz)
    begin
        dsp_cnt <= dsp_cnt + 1;
        if(dsp_cnt == 50000)
        begin
            dsp_cnt <= 0;
            clk_500hz <= ~clk_500hz;
        end
    end


    // write to display
    always @(posedge clk_500hz)
        case(dsp_en)
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
