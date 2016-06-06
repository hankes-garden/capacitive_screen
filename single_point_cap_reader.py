import subprocess
import time
from threading import Thread, Event, Lock
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
import numpy as np
import sys

MAX_BUF_SIZE = 200
g_dataQueue = deque([0 * MAX_BUF_SIZE], maxlen=MAX_BUF_SIZE)
g_readEvent = Event()
g_writeEvent = Event()
g_dataQueueLock = Lock()
g_strFilePath = "./"

def readCapData():
    try:
        hFile = None

        while(g_readEvent.is_set() ):
            # read data
            strData = subprocess.Popen(\
                            "adb shell \"cat /proc/amplitude_log & wait\"",
                            shell=True, stdout=subprocess.PIPE).stdout.read()
            nData = int(strData)

            # add to plot buff
            g_dataQueueLock.acquire()
            g_dataQueue.append(nData)
            g_dataQueueLock.release()

            # write to file
            if (g_writeEvent.is_set() ):
                if (hFile is None):
                    strFileName = dt.datetime.strftime(dt.datetime.now(),
                                                       '%Y%m%d_%H%M%S')
                    hFile = open(g_strFilePath+strFileName+".txt", 'w+')

                hFile.write("%d\n" % nData)
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

def onDraw(frameNum, dataQueue, dataQueueLock, ax):
    # get a copy of data
    dataQueueLock.acquire()
    arrData = np.array(list(dataQueue))
    dataQueueLock.release()

    # plot
    ax.set_data(range(len(arrData) ), arrData)

def main():
    bSave2File = True if int(sys.argv[1]) == 1 else False
    if (bSave2File is True):
        print("save to file is true.\n")
        g_writeEvent.set()

    capReadingThread = None
    try:
        # create & start reading thread
        g_readEvent.set()
        capReadingThread = Thread(target=readCapData, args=())
        capReadingThread.start()

        # setup ploting
        fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=True)
        axes.set_xlim(MAX_BUF_SIZE)
        axes.set_ylim(0, 200)
        axes.set_xlabel("delta")
        ax,  = axes.plot([], [], color='r', lw=2)


        # create animation
        anim = animation.FuncAnimation(fig, onDraw,
                                       fargs=(g_dataQueue,\
                                              g_dataQueueLock,\
                                              ax), interval=100)

        plt.show()

    finally:
        g_readEvent.clear()

    if (capReadingThread is not None):
        capReadingThread.join()



if __name__ == '__main__':
    main()
