# tuning.py

import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 0.5    # range [0.0, 1.0]
fs = 44100      # sampling rate, Hz, must be integer
duration = 10.0  # in seconds, may be float
# generate samples, note conversion to float32 array


def sinfreq(freqfloat):
    "Returns a sine wave for a given frequency float"
    return (np.sin(2*np.pi*np.arange(fs*duration)*freqfloat/fs)).astype(np.float32)


openA = volume*sinfreq(440.0)
openD = volume*sinfreq(293.6)
openG = volume*sinfreq(196.0)
openE = volume*sinfreq(660.0)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=4,
                rate=fs,
                output=True)

# play. May repeat with different volume values


def playstrings():
    for i in [openA, openD, openG, openE]:
        stream.write(volume*i)

        
# playstrings()
# stream.write(volume*openA)
# stream.write(volume*openD)


def tuninga():
    play = True
    if play is True:
        stream.write(volume*openA)

        
def mergearrays(arr1, arr2):  # make for any number of arrays 
    "Merges two arrays of the same length"
    merged = np.ndarray(882000,)
    indexnum = 0
    for i in range(0, 882000, 2):
        merged[i] = (arr1[indexnum])
        merged[i+1] = (arr2[indexnum])
        indexnum += 1
    return merged

        
def dualfreq(freq1, freq2):
    "Returns a sine array for two simultaneous frequencies"
    stream.write(mergearrays(volume*sinfreq(freq1), volume*sinfreq(freq2)))


dualfreq(440.0, 660.0)

dualfreq(293.6, 440.0)

dualfreq(196, 293.6)

dualfreq(293.6, 300.0)
# dualfreq(440.0), volume*sinfreq(441.0))

# tuninga()

stream.stop_stream()
stream.close()

p.terminate()
