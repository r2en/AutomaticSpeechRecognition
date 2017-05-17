#coding: utf-8
import pyaudio
import sys

if len(sys.argv) != 3:
    print "usage: python 3_play.py [raw file] [sampling rate]"
    sys.exit()
rawfile = sys.argv[1]
fs = int(sys.argv[2])


p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(2), channels = 1, rate = fs, output = True)
f = open(rawfile,"rb")
chunk = 1024
data = f.read(chunk)
while stream.is_active():
    stream.write(data)
    data = f.read(chunk)
    if data == '': stream.stop_stream()
stream.close()
p.terminate()