How to get raw capacitance data from touch screen
========
Modern capacitive touch screen detects finger touch via sensing the capacitance changes. To obtain the raw capacitance value from the screen, we need to modify the screen driver which directly communicates with screen controller. Before we start, some preliminaries are needed:

+ Model ID of the taget touch screen (for finding the corresponding screen driver source code).

+ Source code of touch screen driver.

+ Document of the communication protocol used by the screen driver and the screen controller.

+ Basic knowledge of building//downloading customized android system to the mobile deivce. (Cyanogenmod provides an excellent [turtorial](http://wiki.cyanogenmod.org/w/I9100_Info) on this topic)
 
In this project, I implemented a basic code to get raw capacitance data from a Samsung Galaxy SII (i9100), on which the touch screen is Atmel mxt224_u1.

+ The 'mxt224_u1.c' is the modified driver of touch screen, which is modified to retrieve raw cap data from screen controller every 100ms and writes to /proc/amplitude_log (Note that the driver is running in kernel mode while normal application is runing under the user mode. To send data from kernel to user mode, we need to write a file in /proc directory). 

+ The 'cap_reader.py' is a python script which reads the raw data from file and visulaize it in a format of heatmap in a real-time mannar.

