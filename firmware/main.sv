module main(
	 input KEY1, KEY2, KEY3, KEY4,	 
	 output [7:0] rx_data
    );
	 
	 assign rx_data[0] = KEY1;
	 assign rx_data[1] = KEY2;
	 assign rx_data[2] = KEY3;
	 assign rx_data[3] = KEY4;
	 
endmodule