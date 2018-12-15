# /bin/env python3
# -*- coding: utf-8 -*-

"""
Main class for handlng communication with FPGA Board


"""



import serial


class Device(object):
	"""
	"""

	available = False

	def __init__(self, port):
		"""
		initializes USB serial commincation port
		asserts, that the device is ready and responding.
		if there are means it should calibrate the device
		"""
				
		# code
		
		avalable = True
		#end

	def destroy(self):
		"""
		cleans up device
		closes serial port
		
		"""
	
	# TODO properties
	def get_samples(self, value):
		pass
	def set_samples(self):
		pass
		
		
	def read(self, samples=sps):
		pass
	
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

def lookup(self):
	"""
	lookups whether there is any device on any serial bus
	should/could be called before initialization of device
	doesn't belong to Oscilo class, becase it could be called before init
	
	"""
	# iterate through all USBcoms/TTYs
	# try to connect to device
	# try to find version from memmort
	# return list of devices
