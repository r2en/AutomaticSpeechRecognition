#coding: utf-8
import wave
import numpy as np
import pylab as plt
import struct
import pyaudio

# amplitude
amp = 1
# sampling frequency
fs = 8000
# frequency
f0 = 880
# second
sec = 5

swav = []

# create sin wave
for n in np.arange(fs * sec):
    sin = amp * np.sin(2.0 * np.pi * f0 * n / fs)
    swav.append(sin)

# draw sin wave
plt.plot(swav[0:100])
plt.show()

# convert fron -32768 to 32767 : integer
swav = [int(x * 32767.0) for x in swav]

# binary
binwave = struct.pack("h" * len(swav), *swav)

# output file about sin wave
waveFile = wave.Wave_write("audio/440Hz.WAV")
params = (1,2,8000,len(binwave),'NONE','not compressed')
waveFile.setparams(params)
waveFile.writeframes(binwave)
waveFile.close()



