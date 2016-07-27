import sys
import numpy as np
from pylab import *
import scipy.io.wavfile
import matplotlib as mpl
import matplotlib.pyplot as plt
import wave
import copy


def create_wave(song):
    mpl.rcParams['agg.path.chunksize'] = 10000
    rate, data = scipy.io.wavfile.read(song)
    data = copy.deepcopy(data)
    print(data.shape)
    data = np.delete(data, np.s_[::2], 1)
    print(data.shape)



    #x = np.arange(0.0, 2.0, 0.01)
    #data = np.sin(data*x)
    
    plt.plot(data)   
    plt.show()

song = sys.argv[1]
create_wave(song)
