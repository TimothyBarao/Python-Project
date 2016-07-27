import sys
import numpy as np
from pylab import *
import scipy.io.wavfile
import matplotlib as mpl
import matplotlib.pyplot as plt
import wave
import copy


def create_wave(song):
    #np.set_printoptions(threshold=np.inf)
    mpl.rcParams['agg.path.chunksize'] = 10000
    rate, data = scipy.io.wavfile.read(song)
    data = copy.deepcopy(data)
    newdata =np.array([[0,0]])
    blerg = np.array([[0,0]])
    print(data.shape)
    print(data.shape[0])
    
    i = 0
    while 1:
        newdata = np.append(newdata, data[i])
        i += 8000
        if i > data.shape[0]:
            break
        
    print(data.shape)
    print(newdata)
    



    #x = np.arange(0.0, 2.0, 0.01)
    #data = np.sin(data*x)
    
    plt.plot(newdata)   
    plt.show()

song = sys.argv[1]
create_wave(song)
