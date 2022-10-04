#!/usr/bin/python
from pycomm3 import REAL

from PF755Driver import PF755Driver

ip = "10.1.105.16"
print(f"Connecting to: {ip}")
drive = PF755Driver(ip)
drive.open()

port = 0
parameter = 26
value = 9.0

for i in range(20, 40):
    parameter = i
    print(f"Reading Port {port} Parameter # {parameter}")
    ret = drive.read_parameter(port=port, parameter=parameter)
    print(ret)


drive.close()


