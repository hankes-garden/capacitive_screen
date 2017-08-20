How to get raw capacitance data from touch screen
========
Capacitive touch screen detects finger touches via sensing the capacitance changes. To obtain the raw capacitance value from the screen, we need to modify the screen driver and communicate with screen controller. Before we start, some preliminaries are required:

+ Model ID of the taget touch screen.

+ Source file of touch screen driver.

+ Document about communication protocol btw screen driver and screen controller.

+ Basic knowledge of building//downloading customized android to the deivce. The Cyanogenmod provides an excellent [turtorial](http://wiki.cyanogenmod.org/w/I9100_Info) on this topic.
 
This project contains some basic codes to get raw capacitance data from a Samsung Galaxy SII (i9100), whose touch screen is Atmel mxt224_u1.

+ The 'mxt224_u1.c' is the modified driver of touch screen, which retrieves raw data from screen controller every 100ms and writes to /proc/amplitude_log. 

+ The 'cap_reader.py' reads the raw data from device and visulaize it in a format of heatmap in real time.

