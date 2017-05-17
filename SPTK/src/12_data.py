#coding: utf-8
import struct

fp = open("simple.short","wb")
for i in range(100):
    fp.write(struct.pack("h",i))
fp.close()