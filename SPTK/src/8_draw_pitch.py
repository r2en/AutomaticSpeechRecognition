#coding: utf-8
import struct
import sys
from pylab import *

if len(sys.argv) != 2:
    print ('usage: pythn 8_Draw_Pitch.py [pitch file]')
    sys.exit()
pitch_file = sys.argv[1]

pitch = []
f = open(pitch_file,"rb")
while True:
    #float
    b = f.read(4)
    if b == "": break;
    val = struct.unpack("f",b)[0]
    pitch.append(val)
f.close()

plot(range(len(pitch)),pitch)
xlabel("time(frame)")
ylabel("F0 (Hz)")
show()