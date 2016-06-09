How to get raw capacitance data from touch screen
========
To detect touch events, capacitive touch screens sense the capacitance changes caused by finger touches. To get the raw capacitance, we need to modify the screen driver to communicate with touch screen controller. There are something we need to know before starting to do it:

+ Model ID of touch screen, only with it we can find the driver source file and corresponding communication protocol.

+ Source file of touch screen driver, which may be found on the website of its manufactor.

+ Communication protocol btw screen driver and screen controller.

+ The basic knowledge of building//downloading customized android to the deivce. Cyanogenmod provides an excellent [turtorial](http://wiki.cyanogenmod.org/w/I9100_Info) on this topic.


This project contains some basic codes to get raw capacitance data from a Samsung Galaxy SII (i9100), whose touch screen is Atmel mxt224_u1. 

+ The 'mxt224_u1.c' is the modified driver of touch screen, which retrieves raw data from screen controller every 100ms and writes to /proc/amplitude_log. 

+ The 'cap_reader.py' reads the raw data from device and visulaize it in a format of heatmap in real time.

