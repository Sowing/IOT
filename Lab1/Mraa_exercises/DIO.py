import mraa
import time
 
switch_pin_number=8
buzz_pin_number=6
 
# Configuring the switch and buzzer as GPIO interfaces
switch = mraa.Gpio(switch_pin_number)
buzz = mraa.Gpio(buzz_pin_number)
 
# Configuring the switch and buzzer as input & output respectively
switch.dir(mraa.DIR_IN)
buzz.dir(mraa.DIR_OUT)
 
print "Press Ctrl+C to escape..."
try:
        while (1):
                if (switch.read()):     # check if switch pressed
                        buzz.write(1)   # switch on the buzzer
                        time.sleep(0.2) # puts system to sleep for 0.2sec before switching
                        buzz.write(0)   # switch off buzzer
except KeyboardInterrupt:
        exit
