import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.fftpack as fftpack

g_strFilePath = '20160701_143657.txt'

def main():

    # get touch data
    lsTouchValues = []
    with open(g_strFilePath, 'r') as hFile:
        for strLine in hFile:
            lsData = [int(x) for x in strLine.split(',')[:-1] ]
            arrData = np.array(lsData)
            arrFiltered = np.where(arrData>2000, 0, arrData)
            nVal = np.max(arrFiltered)
            lsTouchValues.append(nVal)

    arrTouchVal = np.array(lsTouchValues)

    # fft
    nSamplingFreq = 100
    nSamples = len(arrTouchVal)    
    dRes = nSamplingFreq * 1.0 / nSamples 
    arrFFT = fftpack.fft(arrTouchVal)
    arrNormPower = abs(arrFFT)/(nSamples*1.0)

    # plot 
    fig, axes = plt.subplots(nrows=2, ncols=1, squeeze=True)
    axes[0].plot(arrTouchVal, color='b')
    axes[1].plot(arrNormPower[10:nSamples/2], color='r')
    plt.show()



if __name__ == '__main__':
    main()
