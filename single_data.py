import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack

g_strFilePath = '20160701_143657.txt'

def main():

    # get touch data
    lsTouchValues = []
    with open(g_strFilePath, 'r') as hFile:
        for strLine in hFile:
            lsData = [int(x) for x in strLine.split(',')[:-1] ]
            assert(len(lsData) == 209 )
            arrData = np.array(lsData)
            arrFiltered = np.where(arrData>2000, 0, arrData)
            nVal = np.max(arrFiltered)
            lsTouchValues.append(nVal)

    arrTouchVal = np.array(lsTouchValues)
    
    # fft
    nSamplingFreq = 200
    nSamples = 5*nSamplingFreq
    dRes = nSamplingFreq*1.0/nSamples
    arrFFT = fftpack.fft(arrTouchVal[200: 100+nSamples])
    arrNormPower = abs(arrFFT[:nSamples/2])/(nSamples*1.0)
    

    # plot 
    fig, axes = plt.subplots(nrows=2, ncols=1, squeeze=True)
    axes[0].plot(arrTouchVal, color='b')
    
    
    nDCEnd = 10
    arrFreqIndex = np.linspace(nDCEnd*dRes, nSamplingFreq/2.0,
                               nSamples/2-nDCEnd)
    axes[1].plot(arrFreqIndex, arrNormPower[nDCEnd:], color='r')
    axes[1].set_xticks(range(0, int(nSamplingFreq/2), 10) )
 
    plt.show()



if __name__ == '__main__':
    main()
