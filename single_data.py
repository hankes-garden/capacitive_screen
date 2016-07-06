import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack
import sys

def main():
    strFilePath = sys.argv[1] 

    # get touch data
    lsTouchValues = []
    with open(strFilePath, 'r') as hFile:
        for strLine in hFile:
            lsData = [int(x) for x in strLine.split(',')[:-1] ]
            assert(len(lsData) == 209 )
            arrData = np.array(lsData)
            arrFiltered = np.where(arrData>2000, 0, arrData)
            nVal = np.max(arrFiltered)
            lsTouchValues.append(nVal)

    arrTouchVal = np.array(lsTouchValues)
    
    # fft
    nSamplingFreq = 100
    nFFTStart = 3*nSamplingFreq
    nFFTEnd = nFFTStart + 3*nSamplingFreq
    arrData2FFT = arrTouchVal[nFFTStart:nFFTEnd]

    nSamples = len(arrData2FFT)    
    dRes = nSamplingFreq * 1.0 / nSamples 
    arrFFT = fftpack.fft(arrData2FFT)
    arrNormPower = abs(arrFFT)/(nSamples*1.0)
    nDCEnd = 10
    arrFreqIndex = np.linspace(nDCEnd*dRes, nSamplingFreq/2.0, nSamples/2-nDCEnd)
   

    # plot 
    fig, axes = plt.subplots(nrows=2, ncols=1, squeeze=True)
    axes[0].plot(arrTouchVal, color='b')
    axes[1].plot(arrFreqIndex, arrNormPower[nDCEnd:nSamples/2], color='r')
    plt.show()



if __name__ == '__main__':
    main()
