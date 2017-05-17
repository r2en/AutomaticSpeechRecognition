#coding: utf-8
import wave
import numpy as np
from pylab import *

def dft(start,x,N):
    X = [0.0] * N
    for k in range(N):
        for n in range(N):
            real = np.cos(2 * np.pi * k * n / N)
            imag = - np.sin(2 * np.pi * k * n / N)
            X[k] += x[start + n] * complex(real,imag)
    return X

if __name__ == "__main__":
    wf = wave.open("audio/sine.wav","r")
    fs = wf.getframerate() #sampling frequency
    x = wf.readframes(wf.getnframes())
    x = frombuffer(x,dtype="int16") / 32768.0
    print len(x)
    wf.close()

    start = 0
    N = 256
    x = dft(start,x,N)
    freqList = [k * fs / N for k in range(N)]
    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
    phaseSpectrum = [np.arctan2(int(c.imag),int(c.real)) for c in X]
    