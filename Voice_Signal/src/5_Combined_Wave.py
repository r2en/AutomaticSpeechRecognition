#coding: utf-8
import wave
import struct
import numpy as np
from pylab import *

def createCombinedWave(A,freqList,fs,length):
    data = []
    amp = float(A) / len(freqList)
    for n in arange(length * fs):
        s = 0.0
        for f in freqList:
            s += amp * np.sin(2 * np.pi * f * n / fs)
        if s > 1.0: s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    data = [int(x * 32767.0) for x in data]
    #plot(data[0:100]); show()
    data = struct.pack("h" * len(data), *data)
    return data    

def play(data,fs,bit):
    import pyaudio
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,\
    channels = 1,\
    rate = int(fs),\
    output = True)

    chunk = 1024
    sp = 0
    buffer = data[sp:sp+chunk]
    while buffer != '':
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp:sp+chunk]
    stream.close()
    p.terminate()

def save(data, fs, bit, filename):
    wf = wave.open(filename,"w")
    wf.setnchannels(1)
    wf.setsampwidth(bit/8)
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()

if __name__ == "__main__" :
    chordList = [(262, 330, 392), 
                 (294, 370, 440),  
                 (330, 415, 494), 
                 (349, 440, 523), 
                 (392, 494, 587),  
                 (440, 554, 659), 
                 (494, 622, 740)] 
    for freqList in chordList:
        allData = ""
        data = createCombinedWave(1.0, freqList, 8000.0, 1.0)
        play(data, 8000, 16)
        allData += data
    save(allData, 8000, 16, "audio/combined.wav")

