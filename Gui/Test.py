from pylab import *
from amen.utils import example_audio_file
from amen.audio import Audio
from amen.synthesize import synthesize

import sys
import numpy as np
import scipy.io.wavfile
import matplotlib as mpl
import matplotlib.pyplot as plt
import wave
import copy

def mash(song1, song2):
    audio1 = Audio(song1)
    audio2 = Audio(song2)

    beats1 = audio1.timings['beats']
    beats2 = audio2.timings['beats']

    mashup =[]
    i = 1
    for beat1, beat2 in zip(beats1, beats2):
	    if(i%8 == 7):
		    mashup.append(beat1)
	    else:
		    mashup.append(beat2)
	    i+=1

    out = synthesize(mashup)
    output = 'one_knob.wav'
    out.output(output)
    return output

def create_wave(song):
    mpl.rcParams['agg.path.chunksize'] = 10000
    rate, data = scipy.io.wavfile.read(song)
    data = copy.deepcopy(data)
    newdata =np.array([[0,0]])

    i = 0
    while 1:
        newdata = np.append(newdata, data[i])
        i += 10000
        if i > data.shape[0]:
            break
  
    return newdata

if __name__ == '__main__':
    try:
        song1 = "wav/knob.wav"
        song2 = "wav/time.wav"
        song3 = mash(song1, song2)

        song1_plot = create_wave(song1)
        song2_plot = create_wave(song2)
        song3_plot = create_wave(song3)

        fig = plt.figure()
      
        ax = plt.subplot(311)
        ax.set_title(song1)
        ax.plot(song1_plot)

        ax = plt.subplot(312)
        ax.set_title(song2)
        ax.plot(song2_plot)

        ax = plt.subplot(313)
        ax.set_title(song3)
        ax.plot(song3_plot)

        plt.show()

    except ValueError:
        print('IT ERRORED')
        #mash(audio_file2, audio_file1)

