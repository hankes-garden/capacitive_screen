import subprocess
import rendering
import time
import numpy as np

def PrintRawValues(List):
	subprocess.Popen("clear", shell=True)
	time.sleep(.05);
	print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in List]))

#records until enter is pressed
while True:
    Matrix = np.random.randint(6000, 65536, (11, 19) )
    Points = None


	# use unusable.Calculate(Matrix) to calculate spots that are wet
    rendering.Update(Matrix, Points, [], [], False)	
	







