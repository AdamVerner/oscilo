// This file contains the UART Receiver.  This receiver is able to
// receive 8 bits of serial data, one start bit, one stop bit,
// and no parity bit.  When receive is complete rx_rdwill be
// driven high for one clock cycle.
//
// CLKS_PER_BIT = (Frequency of i_Clock)/(Frequency of UART)
// Example: 10 MHz Clock, 115200 baud UART
// (10*10^6) / 115200 = 87
// (50*10^6) / 115200 = 434
// (50*10^6) / 9600   = 5208

  
module uart_rx 
    #(parameter CLKS_PER_BIT=434)
    (
    input        clk,
    input        rxd,
    output       rx_rd,
    output [7:0] rx_data
    );

    parameter s_IDLE         = 3'b000;
    parameter s_RX_START_BIT = 3'b001;
    parameter s_RX_DATA_BITS = 3'b010;
    parameter s_RX_STOP_BIT  = 3'b011;
    parameter s_CLEANUP      = 3'b100;

    reg [15:0] clk_cnt = 0;
    reg [2:0]  bit_idx = 0;   //8 bits total
    reg [7:0]  r_Rx_Byte = 0; //stage output through register
    reg [2:0]  r_SM_Main = 0;

    // Purpose: Double-register the incoming data.
    // This allows it to be used in the UART RX Clock Domain.
    // (It removes problems caused by metastability)
    reg        rx_r1 = 1'b1;
    reg        rx_r2 = 1'b1;
    always @(posedge clk)
    begin
      rx_r1 <= rxd;
      rx_r2 <= rx_r1;
    end


    // Purpose: Control RX state machine
    always @(posedge clk)
    begin

      case (r_SM_Main)
        s_IDLE :
          begin
            rx_rd <= 1'b0;
            clk_cnt <= 0;
            bit_idx <= 0;

            if (rx_r2 == 1'b0)          // Start bit detected
              r_SM_Main <= s_RX_START_BIT;
            else
              r_SM_Main <= s_IDLE;
          end

        // Check middle of start bit to make sure it's still low
        s_RX_START_BIT :
          begin
            if (clk_cnt == (CLKS_PER_BIT-1)/2)
              begin
                if (rx_r2 == 1'b0)
                  begin
                    clk_cnt <= 0;  // reset counter, found the middle
                    r_SM_Main     <= s_RX_DATA_BITS;
                  end
                else
                  r_SM_Main <= s_IDLE;
              end
            else
              begin
                clk_cnt <= clk_cnt+ 1;
                r_SM_Main     <= s_RX_START_BIT;
              end
          end // case: s_RX_START_BIT


        // Wait CLKS_PER_BIT-1 clock cycles to sample serial data
        s_RX_DATA_BITS :
          begin
            if (clk_cnt < CLKS_PER_BIT-1)
              begin
                clk_cnt <= clk_cnt+ 1;
                r_SM_Main     <= s_RX_DATA_BITS;
              end
            else
              begin
                clk_cnt <= 0;
                r_Rx_Byte[bit_idx] <= rx_r2;

                // Check if we have received all bits
                if (bit_idx < 7)
                  begin
                    bit_idx <= bit_idx+ 1;
                    r_SM_Main   <= s_RX_DATA_BITS;
                  end
                else
                  begin
                    bit_idx <= 0;
                    r_SM_Main   <= s_RX_STOP_BIT;
                  end
              end
          end // case: s_RX_DATA_BITS


        // Receive Stop bit.  Stop bit = 1
        s_RX_STOP_BIT :
          begin
            // Wait CLKS_PER_BIT-1 clock cycles for Stop bit to finish
            if (clk_cnt < CLKS_PER_BIT-1)
              begin
                clk_cnt <= clk_cnt+ 1;
                r_SM_Main     <= s_RX_STOP_BIT;
              end
            else
              begin
                rx_rd       <= 1'b1;
                clk_cnt     <= 0;
                r_SM_Main   <= s_CLEANUP;
              end
          end // case: s_RX_STOP_BIT


        // Stay here 1 clock
        s_CLEANUP :
          begin
            r_SM_Main   <= s_IDLE;
            rx_rd       <= 1'b0;
          end


        default :
          r_SM_Main <= s_IDLE;

      endcase
    end

    assign rx_data = r_Rx_Byte;

endmodule
