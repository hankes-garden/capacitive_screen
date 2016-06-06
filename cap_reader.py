import subprocess
import time
from threading import Thread, Event, Lock
import datetime as dt
import numpy as np
import sys
import rendering

g_arrFrame = np.zeros((11, 19), dtype=int)
g_readEvent = Event()
g_writeEvent = Event()
g_dataLock = Lock()
g_strFilePath = "./"

def readCapData():
    global g_arrFrame

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

            arrData= np.reshape([int(x) for x in lsData], (11, 19) )

            # update plot buff
            g_dataLock.acquire()
            g_arrFrame = np.copy(arrData)
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

def onDraw(frameNum, dataQueue, dataQueueLock, ax):
    # get a copy of data
    dataQueueLock.acquire()
    arrData = np.array(list(dataQueue))
    dataQueueLock.release()

    # plot
    ax.set_data(range(len(arrData) ), arrData)

def main():

    # check whether need to write to file
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

#        # setup ploting
#        fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=True)
#        axes.set_xlim(MAX_BUF_SIZE)
#        axes.set_ylim(0, 200)
#        axes.set_xlabel("delta")
#        ax,  = axes.plot([], [], color='r', lw=2)
#
#
#        # create animation
#        anim = animation.FuncAnimation(fig, onDraw,
#                                       fargs=(g_dataQueue,\
#                                              g_dataLock,\
#                                              ax), interval=100)
#
#        plt.show()

        # rendering
        while(True):
            g_dataLock.acquire()
            arrPlotData = np.copy(g_arrFrame)
            g_dataLock.release()

            rendering.Update(arrPlotData, [], [], [], True)


    finally:
        g_readEvent.clear()

        if (capReadingThread is not None):
            capReadingThread.join()



if __name__ == '__main__':
    main()
