How to get raw capacitance data from touch screen
========
Capacitive touch screens detect finger touch event via sensing the capacitance changes. To get the raw capacitance from device, we need to modify the screen driver to communicate with screen controller. There is something we need to know before doing it:

+ Model ID of taget touch screen, only with it we can locate the driver source file and corresponding communication protocol.

+ Source file of touch screen driver.

+ Document about communication protocol btw screen driver and screen controller.

+ Basic knowledge of building//downloading customized android to the deivce. Cyanogenmod provides an excellent [turtorial](http://wiki.cyanogenmod.org/w/I9100_Info) on this topic.
 
Basically, the screen controller provides various command interfers to support different functions, which


This project contains some basic codes to get raw capacitance data from a Samsung Galaxy SII (i9100), whose touch screen is Atmel mxt224_u1. 

+ The 'mxt224_u1.c' is the modified driver of touch screen, which retrieves raw data from screen controller every 100ms and writes to /proc/amplitude_log. 

+ The 'cap_reader.py' reads the raw data from device and visulaize it in a format of heatmap in real time.

