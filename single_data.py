import signal_filter as sf
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fftpack
import sys

def main():
    strFilePath = sys.argv[1] 

    # get touch data
    lsTouchValues = []
    with open(strFilePath, 'r') as hFile:
        for strLine in hFile:
            lsData = [int(x) for x in strLine.split(',')[:-1] ]
            arrData = np.array(lsData)
            arrFiltered = np.where(arrData>2000, 0, arrData)
            nVal = np.max(arrFiltered)
            lsTouchValues.append(nVal)

    arrTouchVal = np.array(lsTouchValues)
    
    nSamplingFreq = 200
    nDCEnd = 10
    # fft on raw
    arrFreqIndex, arrPower = computeFFT(arrTouchVal, nSamplingFreq, nDCEnd)
                               
                               
    # fft on filtered data
    arrFiltered = sf.butter_highpass_filter(arrTouchVal, 5, nSamplingFreq)
    arrFreqIndex_fil, arrPower_fil = computeFFT(arrFiltered, 
                                                nSamplingFreq, 
                                                nDCEnd)
    
   

    # plot 
    fig, axes = plt.subplots(nrows=4, ncols=1, squeeze=True)
    axes[0].plot(arrTouchVal)
    axes[1].plot(arrFreqIndex, arrPower)
    axes[1].set_xlim((5, 50))
    axes[1].set_ylim((0, 1.5))
    axes[2].plot(arrFiltered)
    axes[3].plot(arrFreqIndex_fil, arrPower_fil)
    fig.suptitle(strFilePath.split('/')[-1])
    plt.show()


def computeFFT(arrData, nSamplingFreq, nDCEnd=10 ):
    nCount = len(arrData)
    dRes = nSamplingFreq*1.0/nCount
    arrFFT = fftpack.fft(arrData)
    arrPower = abs(arrFFT)/(nCount*1.0)
    arrFreqIndex = np.linspace(nDCEnd*dRes, nSamplingFreq/2.0, 
                               nCount/2-nDCEnd)
                               
    return arrFreqIndex, arrPower[nDCEnd: nCount/2]

if __name__ == '__main__':
    main()











