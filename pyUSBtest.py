#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------
# pyUSBtest.py
# Copyright 2016 brainelectronics
# Scharpf, Jonas
# All rights reserved.


import usb
#help(usb.core) 
busses = usb.busses()
for bus in busses:
  devices = bus.devices
  for dev in devices:
    #_name = usb.util.get_string(dev.dev,256,0)  #This is where I'm having trouble
    #print "device name=",_name
    print "Device:", dev.filename
    print "  Device class:",dev.deviceClass
    print "  Device sub class:",dev.deviceSubClass
    print "  Device protocol:",dev.deviceProtocol
    print "  Max packet size:",dev.maxPacketSize
    print "  idVendor:",hex(dev.idVendor)
    print "  idProduct:",hex(dev.idProduct)
    print "  Device Version:",dev.deviceVersion
    for config in dev.configurations:
      print "  Configuration:", config.value
      print "    Total length:", config.totalLength 
      print "    selfPowered:", config.selfPowered
      print "    remoteWakeup:", config.remoteWakeup
      print "    maxPower:", config.maxPower
      for intf in config.interfaces:
        print "    Interface:",intf[0].interfaceNumber
        for alt in intf:
          print "    Alternate Setting:",alt.alternateSetting
          print "      Interface class:",alt.interfaceClass
          print "      Interface sub class:",alt.interfaceSubClass
          print "      Interface protocol:",alt.interfaceProtocol
          for ep in alt.endpoints:
            print "      Endpoint:",hex(ep.address)
            print "        Type:",ep.type
            print "        Max packet size:",ep.maxPacketSize
            print "        Interval:",ep.interval

"""
import sys
import usb.core
# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
	print 'Decimal VendorID=' + str(cfg.idVendor)
	print 'ProductID=' + str(cfg.idProduct)
	print 'Manufacturer=' + str(cfg.iManufacturer)
	print 'Product=' + str(cfg.iProduct)
	print 'Serial=' + str(cfg.iSerialNumber)
"""

"""
import sys
import usb.core
busses = usb.busses()
for bus in busses:
    devices = bus.devices
    for dev in devices:
	print("Device:", dev.filename)
	print("  VID: 0x{:04x}".format(dev.idVendor))
	print("  PID: 0x{:04x}".format(dev.idProduct))
"""


"""
# only for linux
import re
import subprocess
device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb", shell=True)
devices = []
for i in df.split('\n'):
	if i:
		info = device_re.match(i)
		if info:
			dinfo = info.groupdict()
			dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
			devices.append(dinfo)
print devices
"""

"""
# does not list Manufacturer and Serial corretly
import usb

busses = usb.busses()
for bus in busses:
  devices = bus.devices
  for dev in devices:
	print repr(dev)
	print "Device:", dev.filename
	print "  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor)
	print "  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct)
	print "Manufacturer:", dev.iManufacturer
	print "Serial:", dev.iSerialNumber
	print "Product:", dev.iProduct
"""

"""
import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x16c0, idProduct=0x05df)

# was it found?
if dev is None:
	raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
	intf,
	# match the first OUT endpoint
	custom_match = \
	lambda e: \
		usb.util.endpoint_direction(e.bEndpointAddress) == \
		usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
ep.write('test')
"""
"""
import usb.core
import usb.util
import time

def main():
	device = usb.core.find(idVendor=0x16c0, idProduct=0x05df)

	# use the first/default configuration
	device.set_configuration()

	# first endpoint
	endpoint = device[0][(0,0)][0]

	# read a data packet
	data = None
	while True:
		try:
			data = device.read(endpoint.bEndpointAddress,
						   endpoint.wMaxPacketSize)

			RxData = ''.join([chr(x) for x in data])
			print RxData

		except usb.core.USBError as e:
			data = None
			if e.args == ('Operation timed out',):

				continue

if __name__ == '__main__':
	main()
"""
