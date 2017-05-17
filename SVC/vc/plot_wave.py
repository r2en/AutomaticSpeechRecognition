#coding: utf-8
import struct
import sys
from pylab import *
if len(sys.argv) != 2:
    print "usage: python plot_wave.py [raw_file]"
    sys.exit()
raw_file = sys.argv[1]

wave = []
f = open(raw_file,"rb")
while True:
    b = f.read(2)
    if b == "": break;
    val = struct.unpack("h",b)[0]
    wave.append(val)
f.close()

plot(range(len(wave)),wave)
xlabel("sample")
ylabel("amplitude")
xlim([0,len(wave)])
ylim([-32768,32768])
show()