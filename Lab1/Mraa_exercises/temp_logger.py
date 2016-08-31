import mraa
import math
import time
import pyupm_i2clcd as lcd

switch_pin_number=8
switch = mraa.Gpio(switch_pin_number)
switch.dir(mraa.DIR_IN)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.setColor(255, 255, 0)
myLcd.setCursor(0, 0)
myLcd.clear()

print "ctrl+c to quit"

try:
    while(1):
        if (switch.read()):
            tempSensor = mraa.Aio(1)
            a = tempSensor.read()
            R = 1023.0/a-1.0
            R = 100000.0*R
            logd = math.log(R/100000.0)
            Celsius = 1.0/(logd/4275+1/298.15)-273.15
            tempInC = round(Celsius, 2)
            myLcd.clear()
            TempString = str(tempInC)
            print tempInC
            myLcd.write(TempString + " degree")
            time.sleep(1)

except KeyboardInterrupt:
    exit



