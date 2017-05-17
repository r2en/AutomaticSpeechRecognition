#coding: utf-8
import wave
from numpy import *
from pylab import *

def printWaveInfo(wf):
    # Get wave file info
    print "frame:",wf.getnframes()
    print "sampling frequency:",wf.getframerate()
    print "length(sec):",float(wf.getnframes())/wf.getframerate()

if __name__ == '__main__':
    wf = wave.open("audio/440Hz.wav","r")
    printWaveInfo(wf)

    buffer = wf.readframes(wf.getnframes())
    print "1 frame 2 byte * frame = ",len(buffer),"byte"

    data = frombuffer(buffer,dtype = "int16")

    plot(data[0:250])
    show()