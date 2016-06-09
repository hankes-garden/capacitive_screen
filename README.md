Introduction
========
This project contains some basic codes to get raw capacitance data from capacitive touch screen. 

The target device is Samsung Galaxy SII (i9100), whose touch screen is Atmel mxt224_u1. 

To get the raw data, we need to modify its driver and communite with touch screen driver controller. So, before playing with it, we need to be familiar with building/download customized android(cyanogenmod provides an excellent [turtorial](http://wiki.cyanogenmod.org/w/I9100_Info) ) and communitation protocal of Atmel mxt224. 

. The 'mxt224_u1.c' is the modified driver of touch screen, which retrieves raw data from screen controller every 100ms and writes to /proc/amplitude_log. 

. The 'cap_reader.py' reads the raw data from device and visulaize it in a format of heatmap in real time.

