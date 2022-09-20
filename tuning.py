# tuning.py

import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 0.5    # range [0.0, 1.0]
fs = 44100      # sampling rate, Hz, must be integer
duration = 1000.0  # in seconds, may be float


def sinfreq(freqfloat):
    "Returns a sine array for a given frequency float"
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


# def overtone_backend(fundamental, gap, n):
#    if (n < 1)
    
def overtones(fundamental, n=5):
    overtones = [n, ]
    overtones[0] = fundamental
    for i in range(1, n):
        overtones.append(overtones[-1]+fundamental)
    return overtones


def overtonecomposite(fundamental, n=5):
    v = volume
    ots = overtones(fundamental, n)
    otarrs = []
    for i in ots:
        otarrs.append(v*sinfreq(i))
        v *= .5
    stream.write(mergearrays(otarrs).tobytes())

    
def tuninga():
    stream.write(compositefreq(overtones(440.0, 10)))

        
def mergearrays(arrays):
    arraycount = len(arrays)
    arrs = arrays
    merged = np.ndarray(44100*arraycount,)
    indexnum = 0
    for i in range(0, 44100*arraycount, arraycount):
        for j in range(arraycount):
            merged[i+j] = arrs[j][indexnum]
        indexnum += 1
    return merged
        
  
def dualfreq(freq1, freq2):
    "Generates a dual sine wave for two simultaneous frequencies"
    stream.write(mergearrays([volume*sinfreq(freq1), volume*sinfreq(freq2)]))

    
def compositefreq(freqs):
    stream.write(mergearrays(list(map(lambda x: volume*sinfreq(x), freqs))).tobytes())

    
# dualfreq(440.0, 660.0)

# dualfreq(293.6, 440.0)

# dualfreq(196, 293.6)

# dualfreq(293.6, 300.0)

# compositefreq([440.0, 660.0, 880.0])
# dualfreq(440.0), volume*sinfreq(441.0))

# tuninga()


def overtonetest():
    for i in range(10):
        cf = compositefreq(overtones(220.0, i))
        stream.write(cf)

        
# overtonetest()        
overtonecomposite(440.0)

stream.stop_stream()
stream.close()

p.terminate()
