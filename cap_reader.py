import subprocess
from threading import Thread, Event, Lock
import datetime as dt
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

MAX_CAP_VALUE = 300
MIN_CAP_VALUE = 0

g_tpScreenShape = (19, 11) # capacitive sensor resolution

g_arrCapData = np.zeros(g_tpScreenShape, dtype=int)
g_readEvent = Event()       # event for reading from kernel
g_writeEvent = Event()      # event for writing data to file
g_dataLock = Lock()
g_strFilePath = "./"

def readCapData():
    global g_arrCapData

    try:
        hFile = None

        while(g_readEvent.is_set() ):
            # read data
            strData = subprocess.Popen(\
                            "adb shell \"cat /proc/amplitude_log & wait\"",
                            shell=True, stdout=subprocess.PIPE).stdout.read()

            lsData = strData.split(",")[:-1]
            if(len(lsData) != 209 ):
                print("Error, the number of data is invalid: %d.\n" \
                       % len(lsData) )
                continue

            arrData= np.reshape([ int(x) for x in lsData], 
                                 g_tpScreenShape, order='C')
            arrData = np.flipud(arrData)                                         
            arrData = np.where(arrData>=MAX_CAP_VALUE, MAX_CAP_VALUE, arrData)

            # update plot buff
            g_dataLock.acquire()
            g_arrCapData = np.copy(arrData)
            g_dataLock.release()

            # write to file
            if (g_writeEvent.is_set() ):
                if (hFile is None):
                    strFileName = dt.datetime.strftime(dt.datetime.now(),
                                                       '%Y%m%d_%H%M%S')
                    hFile = open(g_strFilePath+strFileName+".txt", 'w+')

                hFile.write("%s\n" % strData)
            elif (hFile is not None):
                hFile.flush()
                hFile.close()
                hFile = None

    finally:
        # close file
        if (hFile is not None):
            hFile.flush()
            hFile.close()
            hFile = None

def onDraw(frameNum, qdMesh):
    arrPlotData = None
    # get a copy of data
    g_dataLock.acquire()
    arrPlotData = np.copy(g_arrCapData)
    g_dataLock.release()

    # plot
    qdMesh.set_array(arrPlotData.ravel() )
    

def main():
    if(len(sys.argv) != 2 ):
        print("Invalid params, usage: python %s bSaveFile.\n" % sys.argv[0] )
        return

    # check whether to save data to file
    bSave2File = True if int(sys.argv[1]) == 1 else False
    if (bSave2File is True):
        print("save to file is true.\n")
        g_writeEvent.set()

    capReadingThread = None
    try:
        # create & start reading thread
        g_readEvent.set()
        capReadingThread = Thread(target=readCapData, args=() )
        capReadingThread.start()

        # setup ploting
        fig, ax = plt.subplots(1)
        ax.set_xlim(0, g_tpScreenShape[1])
        ax.set_ylim(0, g_tpScreenShape[0])
        ax.set_xlabel("delta")
        qdMesh = plt.pcolormesh(np.zeros(g_tpScreenShape, dtype=int),
                                vmin=-50, vmax=MAX_CAP_VALUE,
                                cmap=cm.Blues_r)
        fig.colorbar(qdMesh)

        # create animation
        anim = animation.FuncAnimation(fig, onDraw,
                                       fargs=(qdMesh, ), interval=100)

        plt.show()

    finally:
        g_readEvent.clear()

        if (capReadingThread is not None):
            capReadingThread.join()



if __name__ == '__main__':
    main()
