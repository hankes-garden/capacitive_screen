from graphics import *

GraphicsArray = []
TouchPointGraphicsArray = []


WindowWidth = 480
WindowHeight = 800
PhoneScreenWidth = 480.0
PhoneScreenHeight = 800.0

PreviousList = []
Setup = False


def SetupGraphics(SampleDataObject):
	print "Setup Geaphics"

	global XSize, YSize, Window, GraphicsArray

	#clear everything
	GraphicsArray = []

	Window = GraphWin("Heatmap", WindowWidth, WindowHeight)
	XSize = len(SampleDataObject)
	YSize = len(SampleDataObject[0])

	XSpacing = float(WindowHeight) / float(XSize)
	YSpacing = float(WindowWidth) / float(YSize)


	for x in range(0, XSize):
		GraphicsArray.append([])

		for y in range(0, YSize):
			Shape = Rectangle( Point(y * YSpacing, x * XSpacing), \
                               Point((y + 1) * YSpacing, \
                               (x  +1) * XSpacing) )
			GraphicsArray[x].append(Shape)

			#draw all of the squares black to start
			GraphicsArray[x][y].setFill("#000000")
			Shape.draw(Window)



def DrawShapes(Data, PreviousData, OutlineData, DrawOnChange):
    for x in range(0, XSize):
        for y in range(0, YSize):
            if Data[x][y] != PreviousData[x][y] or DrawOnChange == False:
#               Hex = hex(abs(Data[x][y]+32768))
#               Hex = Hex.replace("0x", "")[:-1]
#               nPadding = 6 - len(Hex)
#               strPadding = ""

               # transform to color hex
               strColor = ""
               nValue = Data[x][y]/4
               if (nValue >= 0 ):
                   strHex = hex(nValue).replace("0x", "")[:-1] \
                       if nValue < 255 else "FF"
                   strHex = "0" + strHex if len(strHex)==1 else strHex
                   strColor = strHex + strHex + strHex
               else:
                   strHex = hex(abs(nValue) ).replace("0x", "")[:-1] \
                            if nValue > -255 else "00"
                   strHex = "0" + strHex if len(strHex)==1 else strHex
                   strColor = "00" + strHex + strHex

               GraphicsArray[x][y].setFill("#"+ strColor)

			#sets up the outlines
            if OutlineData != []:
				if OutlineData[x + 3] != 0:
					GraphicsArray[x][y].setOutline("#440000")

				else:
					GraphicsArray[x][y].setOutline("#000000")

def DrawRealTouchPoints(RealTouchPoints):
	global TouchPointGraphicsArray, Window, PhoneScreenWidth, PhoneScreenHeight, WindowWidth, WindowHeight

	#undraw the previous points
	for i in range(0, len(TouchPointGraphicsArray)):
		TouchPointGraphicsArray[i].undraw()

	#clear the array
	TouchPointGraphicsArray = []

	#draw all of the points
	for i in range(0, len(RealTouchPoints)):
		RealTouchPoints[i][0] = int(float(RealTouchPoints[i][0]) / float(PhoneScreenWidth) * float(WindowWidth));
		RealTouchPoints[i][1] = int(float(RealTouchPoints[i][1]) / float(PhoneScreenHeight) * float(WindowHeight * (30.0 / 27.0)) - (WindowHeight * 3.0 / 27.0));

		Shape = Rectangle(Point(RealTouchPoints[i][0] - 5, RealTouchPoints[i][1] - 5), Point(RealTouchPoints[i][0] + 5, RealTouchPoints[i][1] + 5))
		Shape.setFill("#FF0000")
		Shape.draw(Window)

		#append them to the array for undrawing next time
		TouchPointGraphicsArray.append(Shape)

def DrawOptimizedTouchPoints(OptimizedTouchPointData):
	global TouchPointGraphicsArray, Window, PhoneScreenWidth, PhoneScreenHeight, WindowWidth, WindowHeight

	if OptimizedTouchPointData != -1:
		#draw the optimized points
		for i in range(0, len(OptimizedTouchPointData)):
			OptimizedTouchPointData[i][0] = OptimizedTouchPointData[i][0];
			OptimizedTouchPointData[i][1] = OptimizedTouchPointData[i][1];

			Shape = Rectangle(Point(OptimizedTouchPointData[i][0] - 6, OptimizedTouchPointData[i][1] - 6), Point(OptimizedTouchPointData[i][0] + 6, OptimizedTouchPointData[i][1] + 6))
			Shape.setFill("#00FF00")
			Shape.draw(Window)

			#append them to the array for undrawing next time
			TouchPointGraphicsArray.append(Shape)


def PrintRawValues(List):
	subprocess.Popen("clear", shell=True)
	time.sleep(.05);
	print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in List]))

def Update(MatrixData, TouchPointData,
           OptimizedTouchPointData, OutlineData,
           DrawOnChange):
	global List, PreviousList, Setup

	#Do computation between the old and new list here
	List = MatrixData

	#draws the data to the screen if this is not the first time
	if Setup == True:
		DrawShapes(List, PreviousList, OutlineData, DrawOnChange)
#		#draws all of the real touch points
#		DrawRealTouchPoints(TouchPointData)
#
#		DrawOptimizedTouchPoints(OptimizedTouchPointData)
	#if the data is not setup, setup the graphics
	else:
		SetupGraphics(List)


	#set the previous list to the current list
	PreviousList = List

	Setup = True

def Restart():
	global Window, Setup
	Window.close()
	Setup = False

