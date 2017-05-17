#coding: utf-8
import struct
import sys
from pylab import *

if len(sys.argv) != 2:
    print "usage: python 2_plot.py [raw file]"
    sys.exit()
rawfile = sys.argv[1]

wave = []
file = open(rawfile,"rb")
while True:
    binary = file.read(2)
    if binary == "": break;
    val = struct.unpack("h",binary)[0]
    wave.append(val)
file.close()

plot(range(len(wave)),wave)
xlabel("sample")
ylabel("amplitude")
xlim([0,len(wave)])
ylim([-32768,32767])
show()