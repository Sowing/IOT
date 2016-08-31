#!/usr/bin/env python
import mraa
import math
 
try:
    tempSensor = mraa.Aio(1)
    a = tempSensor.read()
    R = 1023.0/a-1.0
    R = 100000.0*R
    logd = math.log(R/100000.0)
    Celsius = 1.0/(logd/4275+1/298.15)-273.15
    tempInC = round(Celsius, 2)
    print tempInC, "is the current temperature"
except KeyboardInterrupt:
    exit
