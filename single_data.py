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
    
    nSamplingFreq = 100
    nDCEnd = 10
    # fft on raw
    arrFreqIndex, arrPower = computeFFT(arrTouchVal, nSamplingFreq, nDCEnd)
                               
                               
    # fft on filtered data
    arrFiltered = sf.butter_highpass_filter(arrTouchVal, 10, nSamplingFreq)
    arrFreqIndex_fil, arrPower_fil = computeFFT(arrFiltered, 
                                                nSamplingFreq, 
                                                nDCEnd)
    
   

    # plot 
    fig, axes = plt.subplots(nrows=3, ncols=1, squeeze=True)
    axes[0].plot(arrTouchVal, color='b')
    axes[1].plot(arrFreqIndex, arrPower, color='r')
    axes[2].plot(arrFreqIndex_fil, arrPower_fil, color='r')
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











