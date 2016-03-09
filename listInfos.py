#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import usb.core
import usb.util
import sys
 
# find our device
dev = usb.core.find(idVendor=0x16c0, idProduct=0x05df)
 
# was it found?
if dev is None:
	raise ValueError('Device not found')

# configuration will be the active one
dev.set_configuration()
print "Device found!"
print dev

#Read value from device

for bRequest in range(255):
	try:
		read = dev.ctrl_transfer(0x81, bRequest, 0, 0, 8) #read 8 bytes
		print "bRequest ", bRequest
		print read
	except:
		# failed to get data for this request
		pass

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
[Finished in 0.6s]
"""