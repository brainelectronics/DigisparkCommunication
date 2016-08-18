#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------
# talker.py
# Copyright 2016 brainelectronics
# Scharpf, Jonas
# All rights reserved.

import usb.core
import usb.util
import sys
import usb
from usb.util import CTRL_IN, CTRL_OUT, CTRL_TYPE_VENDOR

def getStringDescriptor(device, index):
	"""
	"""
	response = device.ctrl_transfer(usb.util.ENDPOINT_IN,
									usb.legacy.REQ_GET_DESCRIPTOR,
									(usb.util.DESC_TYPE_STRING << 8) | index,
									0, # language id
									255) # length

	# TODO: Refer to 'libusb_get_string_descriptor_ascii' for error handling
	
	return response[2:].tostring().decode('utf-16')

REQUEST_TYPE_SEND = usb.util.build_request_type(usb.util.CTRL_OUT,
												usb.util.CTRL_TYPE_CLASS,
												usb.util.CTRL_RECIPIENT_DEVICE)

REQUEST_TYPE_RECEIVE = usb.util.build_request_type(usb.util.CTRL_IN,
												usb.util.CTRL_TYPE_CLASS,
												usb.util.CTRL_RECIPIENT_DEVICE)

USBRQ_HID_GET_REPORT = 0x01
USBRQ_HID_SET_REPORT = 0x09
CP210x_CONFIG		 = 0xFF
USB_HID_REPORT_TYPE_FEATURE = 0x03
REG_PRODUCT_ID       = 0x3702

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

	def _set_config(self, value, index=0, data=None, request=CP210x_CONFIG):
		# request=CP210x_CONFIG

		# print "value, index, data, request:", value, index, data, request

		res = self.device.ctrl_transfer(
			bmRequestType=CTRL_OUT | CTRL_TYPE_VENDOR,
			bRequest=request, 
			wValue=value, 
			wIndex=index, 
			data_or_wLength=data)

		print "_set_config", res

		# if data is not None and res != len(data):
		# 	raise Cp210xError("Short write (%d of %d bytes)"
		# 					  % (res, len(data)))

	def _set_config_string(self, value, content, max_desc_size):
		assert isinstance(content, basestring)
		encoded = content.encode('utf-16-le')
		desc_size = len(encoded) + 2
		assert desc_size <= max_desc_size
		self._set_config(value, data=chr(desc_size) + "\x03" + encoded)


	def set_product_id(self, pid):
		"""Set the Product ID"""
		assert pid > 0x0000 and pid < 0xFFFF
		self._set_config(REG_PRODUCT_ID, pid)

	def set_product_string(self, product_string):
		"""Set the product string.
		
		The string will be encoded with UTF-16 and must not exceed
		CP210x_MAX_PRODUCT_STRLEN.
		For Unicode Plane 0 (BMP; code points 0-FFFF), this specifies
		the maximum length of the string in characters.
		"""
		self._set_config_string(REG_PRODUCT_STRING, product_string, 
								SIZE_PRODUCT_STRING)
	
	def set_serial_number(self, serial_number):
		"""Set the serial number string.
		
		The string will be encoded with UTF-16 and must not exceed
		CP210x_MAX_SERIAL_STRLEN.
		For Unicode Plane 0 (BMP; code points 0-FFFF), this specifies
		the maximum length of the string in characters.
		"""
		self._set_config_string(REG_SERIAL_NUMBER, serial_number, 
								SIZE_SERIAL_NUMBER)

	def set_version(self, version):
		"""Set the device version .
		"""
		self._set_config(REG_VERSION, to_bcd2(version))


	def _transfer(self, request_type, request, index, value):
		return self.device.ctrl_transfer(
			bmRequestType=request_type, 
			bRequest=request,
			wValue=(USB_HID_REPORT_TYPE_FEATURE << 8) | 0,
			wIndex=index,
			data_or_wLength=value)

	@property
	def productName(self):
		"""
		"""
		return getStringDescriptor(self.device, self.device.iProduct)

	
	@property
	def manufacturer(self):
		"""
		"""
		return getStringDescriptor(self.device, self.device.iManufacturer)



if __name__ == '__main__':
	myArray = []
	myNameArray = []
	myString = ""
	myName = ""
	# theDevice = DigiSparkUsbDevice(idVendor=0x16c0, idProduct=0x486f)
	theDevice = DigiSparkUsbDevice(idVendor=0x16c0, idProduct=0x5056)


	# theDevice = DigiSparkUsbDevice(idVendor=0x10C4, idProduct=0xea69)
	# theDevice = DigiSparkUsbDevice(idVendor=0x1a86, idProduct=0x7523)

	# print ("Found: 0x%04x 0x%04x with product name %s manufactured by %s" 
	# 	%(theDevice.idVendor, 
	# 		theDevice.idProduct,
	# 		theDevice.productName,
	# 		theDevice.manufacturer))
	print ("Found: 0x%04x 0x%04x" 
		%(theDevice.idVendor, 
			theDevice.idProduct))

	# theDevice.set_product_id(pid=0xea69) # works with CP2104

	# """
	# theDevice.write(ord("s"))   # sends '115' aka 's' to simulate
	theDevice.write(ord("m"))   # sends '109' aka 'm' to measure
	# theDevice.write(ord("n"))   # sends '110' aka 'n' to name

	# you have to know exactly how much data is returned if try is not used
	for x in range(0, 30):
		try:
			recDat = chr(theDevice.read())	# convert received to char
			myString += recDat	# append char to previous received
			myArray.append(recDat)	# append to list
		except Exception as e:	# break here
			# print e
			break
	# output data
	print myArray
	print "Returned value: %s" %myString
	# currentValueRead = float(myString.rstrip())
	# print "Received*2: %1.3f" %(currentValueRead*2.0)
	# """

	# theDevice.write(ord("n"))   # sends '110' aka 'n' to get name
	# # you have to know exactly how much data is returned if try is not used
	# for x in range(0, 30):
	# 	try:
	# 		recDat = chr(theDevice.read())	# convert received to char
	# 		myName += recDat	# append char to previous received
	# 		myNameArray.append(recDat)	# append to list
	# 	except Exception as e:	# break here
	# 		break
	
	# # output data
	# print myNameArray
	# print "Returned Name: %s" %myName


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








