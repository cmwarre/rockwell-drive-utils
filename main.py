#!/usr/bin/python
from pycomm3 import REAL, STRING, DINT

from PF755Driver import PF755Driver

ip = "10.1.77.34"
print(f"Connecting to: {ip}")
drive = PF755Driver(ip)
drive.open()
drive.read_parameter(0, 1)
drive.close()


