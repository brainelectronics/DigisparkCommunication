#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------
# listAllDevices.py
# Copyright 2016 brainelectronics
# Scharpf, Jonas
# All rights reserved.

import usb.core
import usb.util
import sys
import time

class UsbLister(object):
	"""docstring for UsbLister"""
	def __init__(self):
		super(UsbLister, self).__init__()
		# find USB devices
		# self.dev = usb.core.find(find_all=True)
		# print "Found %d devices" %sum(1 for e in self.dev)
		self.myDict = {}	# general dict of all available devices
		self.myDevices ={}	# dict of named deviceds

		# # search again...
		self.dev = usb.core.find(find_all=True)
		# was anything found?
		if self.dev is None:
			raise ValueError('Device not found')

	def listDevices(self):
		# loop through devices, printing general infos in decimal and hex
		devNum = 1
		for cfg in self.dev:
			# print devNum
			# print "VendorID: 0x%04x (%d)" %(cfg.idVendor, cfg.idVendor)
			# print "ProductID: 0x%04x (%d)" %(cfg.idProduct, cfg.idProduct)
			# print "Manufacturer: 0x%04x (%d)" %(cfg.iManufacturer, cfg.iManufacturer)
			# print "Product: 0x%04x (%d)" %(cfg.iProduct, cfg.iProduct)
			# print "Serial: 0x%04x (%d)" %(cfg.iSerialNumber, cfg.iSerialNumber)

			# print "Complete Device Infos"
			# print cfg
			# print ""

			self.myDict[devNum] = [cfg.idVendor, cfg.idProduct]
			devNum += 1

		# print self.myDict

		# get device name and manufacturer name
		for aDev in self.myDict:
			self.solveDeviceName(self.myDict[aDev][0],self.myDict[aDev][1])
			# time.sleep(0.5)

	def solveDeviceName(self, idVen, idProd):
		"""
		request device name and manufacturer name if available
		"""
		device = usb.core.find(idVendor=idVen,
									idProduct=idProd)

		# only try to get a name
		try:
			productName = str(self.getStringDescriptor(device, device.iProduct))
			print productName,
			print "by %s" %self.getStringDescriptor(device, device.iManufacturer),
			print "at Ven: %s and Prod: %s" %(idVen, idProd)
			self.myDevices[productName] = [idVen, idProd]
		except Exception as e:
			# pass if no name or manufacturer is available
			pass

	def getDevices(self):
		return self.myDevices

	def getStringDescriptor(self, device, index):
		response = device.ctrl_transfer(usb.util.ENDPOINT_IN,
										usb.legacy.REQ_GET_DESCRIPTOR,
										(usb.util.DESC_TYPE_STRING << 8) | index,
										0, # language id
										255) # length
		
		return response[2:].tostring().decode('utf-16')

if __name__ == '__main__':
	theDevices = UsbLister()
	theDevices.listDevices()
	tmpDict = theDevices.getDevices()
	print "Device dict: %s" %tmpDict
	print "Device dict keys: %s" %tmpDict.keys()

# sample output
"""
Device found!
DEVICE ID 16c0:05df on Bus 004 Address 003 =================
 bLength                :   0x12 (18 bytes)
 bDescriptorType        :    0x1 Device
 bcdUSB                 :  0x110 USB 1.1
 bDeviceClass           :    0x0 Specified at interface
 bDeviceSubClass        :    0x0
 bDeviceProtocol        :    0x0
 bMaxPacketSize0        :    0x8 (8 bytes)
 idVendor               : 0x16c0
 idProduct              : 0x05df
 bcdDevice              :  0x100 Device 1.0
 iManufacturer          :    0x1 digistump.com
 iProduct               :    0x2 DigiUSB
 iSerialNumber          :    0x0 
 bNumConfigurations     :    0x1
	CONFIGURATION 1: 100 mA ==================================
	 bLength              :    0x9 (9 bytes)
	 bDescriptorType      :    0x2 Configuration
	 wTotalLength         :   0x22 (34 bytes)
	 bNumInterfaces       :    0x1
	 bConfigurationValue  :    0x1
	 iConfiguration       :    0x0 
	 bmAttributes         :   0x80 Bus Powered
	 bMaxPower            :   0x32 (100 mA)
		INTERFACE 0: Human Interface Device ====================
		 bLength            :    0x9 (9 bytes)
		 bDescriptorType    :    0x4 Interface
		 bInterfaceNumber   :    0x0
		 bAlternateSetting  :    0x0
		 bNumEndpoints      :    0x1
		 bInterfaceClass    :    0x3 Human Interface Device
		 bInterfaceSubClass :    0x0
		 bInterfaceProtocol :    0x0
		 iInterface         :    0x0 
			ENDPOINT 0x81: Interrupt IN ==========================
			 bLength          :    0x7 (7 bytes)
			 bDescriptorType  :    0x5 Endpoint
			 bEndpointAddress :   0x81 IN
			 bmAttributes     :    0x3 Interrupt
			 wMaxPacketSize   :    0x8 (8 bytes)
			 bInterval        :    0xa
DigiPV digistump.com
[Finished in 0.6s]
"""