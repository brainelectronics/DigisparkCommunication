# DigisparkCommunication
=======
A simple Python script to communicate with the Digispark via USB

- Change the Vendor ID and Product ID to fit your device
- run the listInfos.py script for further infos of the device (you have to run it with sudo on Linux to get everything)
- check out the talker.py script for simple reference how to communicate with the Digispark (upload Digispark_simple_com.ino first)
- use listAllDevices.py to list all devices and return their name and manufacturer name (you have to run it with sudo on Linux to get everything)

Also available in ev-charge-control/Examples/PyUSB<br>
You need to install pyusb and libsub:<br>
sudo pip install pyusb --pre<br>
sudo apt-get install libsub-1.0-0-dev (may you can use auto complete)
