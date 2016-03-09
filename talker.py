#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import usb.core
import usb.util
import sys
import usb


REQUEST_TYPE_SEND = usb.util.build_request_type(usb.util.CTRL_OUT,
												usb.util.CTRL_TYPE_CLASS,
												usb.util.CTRL_RECIPIENT_DEVICE)

REQUEST_TYPE_RECEIVE = usb.util.build_request_type(usb.util.CTRL_IN,
												usb.util.CTRL_TYPE_CLASS,
												usb.util.CTRL_RECIPIENT_DEVICE)

USBRQ_HID_GET_REPORT = 0x01
USBRQ_HID_SET_REPORT = 0x09
USB_HID_REPORT_TYPE_FEATURE = 0x03

class DigiSparkUsbDevice(object):
	"""
	"""
	def __init__(self, idVendor, idProduct):
		self.idVendor = idVendor
		self.idProduct = idProduct

		# TODO: Make more compliant by checking serial number also.
		self.device = usb.core.find(idVendor=self.idVendor,
									idProduct=self.idProduct)

		if not self.device:
			raise Exception("Device not found")

	def write(self, byte):
		"""
		write byte to port
		"""
		# TODO: Return bytes written
		print "Wrote to port: " + str(byte)
		self._transfer(
			request_type=REQUEST_TYPE_SEND, 
			request=USBRQ_HID_SET_REPORT,
			index=byte,
			value=[]) # ignored

	def read(self):
		"""
		read from device
		"""
		response = self._transfer(
			request_type=REQUEST_TYPE_RECEIVE, 
			request=USBRQ_HID_GET_REPORT,
			index=0, # ignored
			value=1) # length

		# if not response:
		# 	raise Exception("No Data")
		# return response[0]

		if response:	# only return value if there was a response
			return response[0]

	def _transfer(self, request_type, request, index, value):
		return self.device.ctrl_transfer(
			bmRequestType=request_type, 
			bRequest=request,
			wValue=(USB_HID_REPORT_TYPE_FEATURE << 8) | 0,
			wIndex=index,
			data_or_wLength=value)


if __name__ == '__main__':
	myArray = []
	myString = ""
	theDevice = DigiSparkUsbDevice(idVendor=0x16c0, idProduct=0x05df)
	theDevice.write(ord("s"))   # sends '115' aka 's' to start

	# you have to know exactly how much data is returned if try is not used
	for x in range(0, 30):
		try:
			recDat = chr(theDevice.read())	# convert received to char
			myString += recDat	# append char to previous received
			myArray.append(recDat)	# append to list
		except Exception as e:	# break here
			break
	
	# output data
	print myArray
	print myString


	"""
	83		S
	116		t
	97		a
	114		r
	116		t
	13		CR
	10 		LF
	82		R
	101		e
	100		d
	32		SPACE
	49		1
	49		1
	53		5
	13		CR
	10 		LF
	71		G
	114		r
	101		e
	101		e
	110		n
	32		SPACE
	49		1
	49		1
	53		5
	13		CR
	10 		LF
	66		B
	108		l
	117		u
	101		e
	32		SPACE
	49		1
	49		1
	53		5
	13		CR
	10 		LF
	----------------
	83		S
	116		t
	97		a
	114		r
	116		t
	13		CR
	10 		LF
	82		R
	101		e
	100		d
	"""








