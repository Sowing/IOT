import mraa
import time
 
switch_pin_number=8
buzz_pin_number=6
 
 
# We define the Interrupt Function here.
# This function is executed everytime an interrupt is triggered.
 
def interr_test(args):
        buzz.write(1)
        time.sleep(0.2)
        buzz.write(0)
 
 
switch = mraa.Gpio(switch_pin_number)
buzz = mraa.Gpio(buzz_pin_number)
 
# Configuring the switch to input & buzzer to output respectively
switch.dir(mraa.DIR_IN)
buzz.dir(mraa.DIR_OUT)
 
#The command below enables the interrupt.
switch.isr(mraa.EDGE_RISING, interr_test, interr_test)
 
# The interrupt is going to be valid for as long as the program runs
# Therefore we setup a dummy "do-nothing" condition
try:
        while(1):
                pass    #"do-nothing" condition
except KeyboardInterrupt:
        buzz.write(0)
        exit
