#coding: utf-8

import struct
import sys
from pylab import *

if len(sys.argv) != 4:
    print "usage python plot_fft.py [fft_file] [N] [fs]"
    sys.exit()

fftfile = sys.argv[1]
N =int(sys.argv[2])
fs = int(sys.argv[3])

fft = []
f = open(fftfile,"rb")
while True:
    b = f.read(4)
    if b == "": break;
    val = struct.unpack("f",b)[0]
    fft.append(val)
f.close()

freqList = np.fft.fftfreq(N,d=1.0/fs)

plot(freqList[:N/2],fft[:N/2])
xlim([0,fs/2])

xlabel("frequency [Hz]")
ylabel("amplitude spectrum")
show()

