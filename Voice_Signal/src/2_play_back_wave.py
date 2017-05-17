'''
sineWithNoise.wav
440Hz is consist of A
This audio file is 440Hz's sine wave 
1/2 * sin(2 * pi * 440 * x) + randomGauss(0,0.1)
'''

#coding: utf-8
import wave
import pyaudio

def printWaveInfo(wf):
    # Get wave information
    print "channle:",wf.getnchannels()
    print "sampling frequency:",wf.getframerate()
    print "frame:",wf.getnframes()
    print "parameter:",wf.getparams()
    print "length(sec):",float(wf.getnframes())/wf.getframerate()

if __name__ == '__main__':
    wf = wave.open("audio/combined.wav","r")
    printWaveInfo(wf)

    # Open Stream
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),\
    channels = wf.getnchannels(),\
    rate = wf.getframerate(),\
    output = True)

    # output astream and play back audio
    chunk = 1024
    data  = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()

